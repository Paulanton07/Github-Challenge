"""
Stripe payment integration services
"""
import stripe
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from .models import PaymentAccount, StripeCustomer, PaymentTransaction, EscrowAccount
from projects.models import Project
from investments.models import Investment
import logging

logger = logging.getLogger(__name__)

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def get_or_create_stripe_customer(user):
    """Get or create Stripe customer for user"""
    try:
        stripe_customer = user.stripe_customer
        return stripe_customer.stripe_customer_id
    except StripeCustomer.DoesNotExist:
        # Create new Stripe customer
        if settings.SANDBOX_MODE:
            # Mock customer ID for sandbox
            customer_id = f"cus_sandbox_{user.id}"
            logger.info(f"[SANDBOX] Created mock customer: {customer_id}")
        else:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.username,
                metadata={'user_id': user.id}
            )
            customer_id = customer.id
        
        # Save to database
        StripeCustomer.objects.create(
            user=user,
            stripe_customer_id=customer_id
        )
        
        return customer_id


def create_or_get_stripe_account(user):
    """Create or retrieve Stripe Connect account for project creator"""
    try:
        payment_account = user.payment_account
        return payment_account.stripe_account_id
    except PaymentAccount.DoesNotExist:
        # Create new Stripe Connect account
        if settings.SANDBOX_MODE:
            # Mock account ID for sandbox
            account_id = f"acct_sandbox_{user.id}"
            logger.info(f"[SANDBOX] Created mock Connect account: {account_id}")
        else:
            account = stripe.Account.create(
                type='express',
                country='ZA',
                email=user.email,
                capabilities={
                    'card_payments': {'requested': True},
                    'transfers': {'requested': True},
                },
                metadata={'user_id': user.id}
            )
            account_id = account.id
        
        # Save to database
        PaymentAccount.objects.create(
            user=user,
            stripe_account_id=account_id,
            account_type='express'
        )
        
        return account_id


def create_stripe_account_link(user, refresh_url, return_url):
    """Generate Stripe Connect onboarding link"""
    account_id = create_or_get_stripe_account(user)
    
    if settings.SANDBOX_MODE:
        # In sandbox mode, auto-complete onboarding
        payment_account = user.payment_account
        payment_account.onboarding_complete = True
        payment_account.charges_enabled = True
        payment_account.payouts_enabled = True
        payment_account.save()
        
        logger.info(f"[SANDBOX] Auto-completed onboarding for {user.username}")
        return return_url  # Skip onboarding, go straight to return URL
    else:
        account_link = stripe.AccountLink.create(
            account=account_id,
            refresh_url=refresh_url,
            return_url=return_url,
            type='account_onboarding',
        )
        return account_link.url


def create_investment_payment_intent(investment):
    """Create Stripe Payment Intent for investment"""
    investor = investment.investor
    project = investment.project
    amount = investment.amount
    
    # Get or create customer
    customer_id = get_or_create_stripe_customer(investor)
    
    if settings.SANDBOX_MODE:
        # Mock payment intent for sandbox
        intent_id = f"pi_sandbox_{investment.id}"
        client_secret = f"{intent_id}_secret"
        
        logger.info(f"[SANDBOX] Created mock payment intent: {intent_id} for R{amount}")
        
        # Auto-complete the payment in sandbox mode
        investment.status = 'completed'
        investment.payment_reference = intent_id
        investment.save()
        
        # Update project funding
        project.current_funding += amount
        if project.current_funding >= project.funding_goal:
            project.status = 'funded'
        project.save()
        
        # Create transaction record
        PaymentTransaction.objects.create(
            transaction_id=intent_id,
            user=investor,
            investment=investment,
            amount=amount,
            transaction_type='investment',
            status='succeeded',
            payment_method='sandbox_card',
            processor_response={'sandbox': True, 'auto_completed': True}
        )
        
        # Update or create escrow
        escrow, created = EscrowAccount.objects.get_or_create(
            project=project,
            defaults={'status': 'active'}
        )
        escrow.total_held += amount
        if intent_id not in escrow.stripe_payment_intent_ids:
            escrow.stripe_payment_intent_ids.append(intent_id)
        escrow.save()
        
        return {
            'id': intent_id,
            'client_secret': client_secret,
            'status': 'succeeded',
            'sandbox': True
        }
    else:
        # Real Stripe payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency='zar',
            customer=customer_id,
            metadata={
                'investment_id': investment.id,
                'project_id': project.id,
                'investor_id': investor.id,
            },
            # Hold funds in escrow (capture manually later when goal reached)
            capture_method='manual',
        )
        
        # Update investment with payment reference
        investment.payment_reference = intent.id
        investment.save()
        
        # Create transaction record
        PaymentTransaction.objects.create(
            transaction_id=intent.id,
            user=investor,
            investment=investment,
            amount=amount,
            transaction_type='investment',
            status='pending',
            payment_method='card',
            processor_response={'payment_intent': intent.id}
        )
        
        return {
            'id': intent.id,
            'client_secret': intent.client_secret,
            'status': intent.status,
            'sandbox': False
        }


def release_escrow_to_creator(project):
    """Release escrowed funds to project creator when goal is reached"""
    if project.current_funding < project.funding_goal:
        raise ValueError("Funding goal not reached")
    
    try:
        escrow = project.escrow
    except EscrowAccount.DoesNotExist:
        raise ValueError("No escrow account found for this project")
    
    if escrow.status != 'active' and escrow.status != 'funded':
        raise ValueError(f"Cannot release escrow with status: {escrow.status}")
    
    # Calculate platform fee
    platform_fee = (escrow.total_held * Decimal(str(settings.PLATFORM_FEE_PERCENTAGE))) / 100
    creator_amount = escrow.total_held - platform_fee
    
    if settings.SANDBOX_MODE:
        # Mock transfer for sandbox
        transfer_id = f"tr_sandbox_{project.id}"
        
        logger.info(f"[SANDBOX] Released R{creator_amount} to {project.creator.username}")
        logger.info(f"[SANDBOX] Platform fee: R{platform_fee}")
        
        # Update escrow
        escrow.status = 'released'
        escrow.total_released = creator_amount
        escrow.platform_fee_collected = platform_fee
        escrow.released_at = timezone.now()
        escrow.save()
        
        # Record platform fee transaction
        PaymentTransaction.objects.create(
            transaction_id=f"fee_{transfer_id}",
            user=project.creator,
            amount=platform_fee,
            transaction_type='platform_fee',
            status='succeeded',
            processor_response={'sandbox': True}
        )
        
        return {'id': transfer_id, 'amount': float(creator_amount), 'sandbox': True}
    else:
        # Get creator's Stripe account
        try:
            creator_account = project.creator.payment_account
        except PaymentAccount.DoesNotExist:
            raise ValueError("Project creator has not set up payment account")
        
        # Capture all payment intents
        for payment_intent_id in escrow.stripe_payment_intent_ids:
            stripe.PaymentIntent.capture(payment_intent_id)
        
        # Create transfer to creator
        transfer = stripe.Transfer.create(
            amount=int(creator_amount * 100),
            currency='zar',
            destination=creator_account.stripe_account_id,
            metadata={
                'project_id': project.id,
                'type': 'funding_release',
            }
        )
        
        # Update escrow
        escrow.status = 'released'
        escrow.total_released = creator_amount
        escrow.platform_fee_collected = platform_fee
        escrow.released_at = timezone.now()
        escrow.save()
        
        # Record platform fee
        PaymentTransaction.objects.create(
            transaction_id=f"fee_{transfer.id}",
            user=project.creator,
            amount=platform_fee,
            transaction_type='platform_fee',
            status='succeeded'
        )
        
        return transfer


def refund_failed_campaign(project):
    """Refund all investors if campaign fails"""
    if project.status != 'cancelled':
        raise ValueError("Project must be cancelled to refund")
    
    try:
        escrow = project.escrow
    except EscrowAccount.DoesNotExist:
        logger.warning(f"No escrow account found for project {project.id}")
        return []
    
    escrow.status = 'refunding'
    escrow.save()
    
    refunded_investments = []
    
    if settings.SANDBOX_MODE:
        # Mock refunds for sandbox
        for investment in project.investments.filter(status='completed'):
            logger.info(f"[SANDBOX] Refunding R{investment.amount} to {investment.investor.username}")
            
            # Update investment status
            investment.status = 'refunded'
            investment.save()
            
            # Update transaction
            try:
                transaction = PaymentTransaction.objects.get(
                    transaction_id=investment.payment_reference
                )
                transaction.status = 'refunded'
                transaction.save()
            except PaymentTransaction.DoesNotExist:
                pass
            
            refunded_investments.append(investment)
        
        # Update project funding
        project.current_funding = 0
        project.save()
        
    else:
        # Real Stripe refunds
        for payment_intent_id in escrow.stripe_payment_intent_ids:
            try:
                # Cancel uncaptured payment intent (releases authorization)
                stripe.PaymentIntent.cancel(payment_intent_id)
                
                # Update investment status
                investment = Investment.objects.get(payment_reference=payment_intent_id)
                investment.status = 'refunded'
                investment.save()
                
                # Update transaction
                transaction = PaymentTransaction.objects.get(transaction_id=payment_intent_id)
                transaction.status = 'refunded'
                transaction.save()
                
                refunded_investments.append(investment)
                
            except Exception as e:
                logger.error(f"Refund failed for {payment_intent_id}: {e}")
    
    # Update escrow
    escrow.status = 'refunded'
    escrow.refunded_at = timezone.now()
    escrow.save()
    
    return refunded_investments
