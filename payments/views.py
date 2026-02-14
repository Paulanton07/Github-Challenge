from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from decimal import Decimal
import stripe
import logging

from projects.models import Project
from investments.models import Investment
from .models import PaymentTransaction, EscrowAccount
from .services import (
    create_stripe_account_link,
    create_investment_payment_intent,
    release_escrow_to_creator,
    refund_failed_campaign
)

logger = logging.getLogger(__name__)


@login_required
def connect_stripe_account(request):
    """Initiate Stripe Connect onboarding for project creators"""
    refresh_url = request.build_absolute_uri(reverse('stripe_connect_refresh'))
    return_url = request.build_absolute_uri(reverse('stripe_connect_return'))
    
    try:
        account_link_url = create_stripe_account_link(
            request.user,
            refresh_url,
            return_url
        )
        
        if settings.SANDBOX_MODE and account_link_url == return_url:
            # Sandbox mode auto-completed
            messages.success(request, '[SANDBOX MODE] Payment account connected successfully!')
            return redirect('stripe_connect_return')
        
        return redirect(account_link_url)
        
    except Exception as e:
        logger.error(f"Stripe Connect error: {e}")
        messages.error(request, f'Error connecting payment account: {str(e)}')
        return redirect('dashboard')


@login_required
def stripe_connect_refresh(request):
    """Handle Stripe Connect refresh (user needs to complete onboarding again)"""
    messages.warning(request, 'Please complete the payment account setup.')
    return redirect('connect_stripe_account')


@login_required
def stripe_connect_return(request):
    """Handle successful Stripe Connect onboarding"""
    messages.success(request, 'Payment account connected successfully! You can now receive funds.')
    return redirect('dashboard')


@login_required
def make_investment_payment(request, project_id):
    """Process investment payment"""
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', 0))
            
            # Validate amount
            if amount < Decimal(str(settings.MIN_INVESTMENT_AMOUNT)):
                messages.error(request, f'Minimum investment is R{settings.MIN_INVESTMENT_AMOUNT}')
                return redirect('project_detail', pk=project_id)
            
            if amount > Decimal(str(settings.MAX_INVESTMENT_AMOUNT)):
                messages.error(request, f'Maximum investment is R{settings.MAX_INVESTMENT_AMOUNT}')
                return redirect('project_detail', pk=project_id)
            
            # Check if project is active
            if not project.is_active:
                messages.error(request, 'This project is no longer accepting investments.')
                return redirect('project_detail', pk=project_id)
            
            # Create Investment record
            investment = Investment.objects.create(
                investor=request.user,
                project=project,
                amount=amount,
                status='pending'
            )
            
            # Create payment intent
            payment_data = create_investment_payment_intent(investment)
            
            if settings.SANDBOX_MODE:
                # In sandbox mode, payment is auto-completed
                messages.success(request, f'[SANDBOX] Successfully invested R{amount} in {project.title}!')
                return redirect('investment_success', investment_id=investment.id)
            else:
                # Real Stripe checkout
                return render(request, 'payments/checkout.html', {
                    'investment': investment,
                    'project': project,
                    'client_secret': payment_data['client_secret'],
                    'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
                })
        
        except Exception as e:
            logger.error(f"Investment payment error: {e}")
            messages.error(request, f'Payment error: {str(e)}')
            return redirect('project_detail', pk=project_id)
    
    return redirect('project_detail', pk=project_id)


@login_required
def investment_success(request, investment_id):
    """Handle successful investment"""
    investment = get_object_or_404(Investment, id=investment_id, investor=request.user)
    
    return render(request, 'payments/investment_success.html', {
        'investment': investment,
        'project': investment.project,
    })


@login_required
def payment_history(request):
    """View user's payment transaction history"""
    transactions = PaymentTransaction.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'transactions': transactions,
        'sandbox_mode': settings.SANDBOX_MODE,
    }
    return render(request, 'payments/payment_history.html', context)


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    
    if not settings.STRIPE_WEBHOOK_SECRET:
        logger.warning("Stripe webhook secret not configured")
        return HttpResponse(status=400)
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        logger.error("Invalid webhook payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid webhook signature")
        return HttpResponse(status=400)
    
    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        handle_payment_success(payment_intent)
    
    elif event.type == 'payment_intent.payment_failed':
        payment_intent = event.data.object
        handle_payment_failure(payment_intent)
    
    elif event.type == 'account.updated':
        account = event.data.object
        handle_account_update(account)
    
    return HttpResponse(status=200)


def handle_payment_success(payment_intent):
    """Process successful payment"""
    investment_id = payment_intent.metadata.get('investment_id')
    
    if not investment_id:
        logger.warning(f"No investment_id in payment intent {payment_intent.id}")
        return
    
    try:
        investment = Investment.objects.get(id=investment_id)
        investment.status = 'completed'
        investment.save()
        
        # Update project funding
        project = investment.project
        project.current_funding += investment.amount
        if project.current_funding >= project.funding_goal:
            project.status = 'funded'
        project.save()
        
        # Update transaction record
        transaction = PaymentTransaction.objects.get(transaction_id=payment_intent.id)
        transaction.status = 'succeeded'
        transaction.processor_response = payment_intent
        transaction.save()
        
        # Update escrow
        escrow, created = EscrowAccount.objects.get_or_create(
            project=project,
            defaults={'status': 'active'}
        )
        escrow.total_held += investment.amount
        if payment_intent.id not in escrow.stripe_payment_intent_ids:
            escrow.stripe_payment_intent_ids.append(payment_intent.id)
        escrow.save()
        
        logger.info(f"Payment succeeded for investment {investment.id}")
        
    except Investment.DoesNotExist:
        logger.error(f"Investment {investment_id} not found")
    except Exception as e:
        logger.error(f"Error handling payment success: {e}")


def handle_payment_failure(payment_intent):
    """Process failed payment"""
    investment_id = payment_intent.metadata.get('investment_id')
    
    if not investment_id:
        return
    
    try:
        investment = Investment.objects.get(id=investment_id)
        investment.status = 'failed'
        investment.save()
        
        # Update transaction record
        transaction = PaymentTransaction.objects.get(transaction_id=payment_intent.id)
        transaction.status = 'failed'
        transaction.error_message = payment_intent.last_payment_error.get('message', '') if payment_intent.last_payment_error else ''
        transaction.save()
        
        logger.warning(f"Payment failed for investment {investment.id}")
        
    except Investment.DoesNotExist:
        logger.error(f"Investment {investment_id} not found")
    except Exception as e:
        logger.error(f"Error handling payment failure: {e}")


def handle_account_update(account):
    """Process Stripe account updates"""
    try:
        from .models import PaymentAccount
        payment_account = PaymentAccount.objects.get(stripe_account_id=account.id)
        
        # Update account status
        payment_account.charges_enabled = account.charges_enabled
        payment_account.payouts_enabled = account.payouts_enabled
        payment_account.onboarding_complete = account.details_submitted
        payment_account.save()
        
        logger.info(f"Updated payment account {account.id}")
        
    except PaymentAccount.DoesNotExist:
        logger.warning(f"Payment account {account.id} not found")
    except Exception as e:
        logger.error(f"Error handling account update: {e}")
