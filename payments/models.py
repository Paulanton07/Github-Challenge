from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal


class PaymentAccount(models.Model):
    """Stripe Connect account for project creators to receive funds"""
    ACCOUNT_TYPE_CHOICES = [
        ('express', 'Express'),
        ('standard', 'Standard'),
        ('custom', 'Custom'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_account'
    )
    stripe_account_id = models.CharField(max_length=255, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='express')
    
    onboarding_complete = models.BooleanField(default=False)
    charges_enabled = models.BooleanField(default=False)
    payouts_enabled = models.BooleanField(default=False)
    
    capabilities_enabled = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Payment Account'
        verbose_name_plural = 'Payment Accounts'
    
    def __str__(self):
        return f"{self.user.username} - {self.stripe_account_id}"


class StripeCustomer(models.Model):
    """Stripe customer record for investors"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stripe_customer'
    )
    stripe_customer_id = models.CharField(max_length=255, unique=True)
    
    default_payment_method = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Stripe Customer'
        verbose_name_plural = 'Stripe Customers'
    
    def __str__(self):
        return f"{self.user.username} - {self.stripe_customer_id}"


class PaymentTransaction(models.Model):
    """Track all payment transactions through Stripe"""
    TRANSACTION_TYPE_CHOICES = [
        ('investment', 'Investment'),
        ('dividend', 'Dividend Payout'),
        ('refund', 'Refund'),
        ('platform_fee', 'Platform Fee'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    transaction_id = models.CharField(max_length=255, unique=True)  # Stripe ID
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_transactions'
    )
    investment = models.ForeignKey(
        'investments.Investment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payment_transactions'
    )
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='ZAR')
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    payment_method = models.CharField(max_length=50, blank=True)
    processor_response = models.JSONField(default=dict, blank=True)
    
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment Transaction'
        verbose_name_plural = 'Payment Transactions'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', 'transaction_type']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.transaction_type} - {self.user.username} - R{self.amount} ({self.status})"


class EscrowAccount(models.Model):
    """Track funds held in escrow for projects"""
    STATUS_CHOICES = [
        ('active', 'Active - Collecting Funds'),
        ('funded', 'Funded - Goal Reached'),
        ('released', 'Released to Creator'),
        ('refunding', 'Refunding Investors'),
        ('refunded', 'Refunded'),
    ]
    
    project = models.OneToOneField(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='escrow'
    )
    
    stripe_payment_intent_ids = models.JSONField(default=list, blank=True)
    
    total_held = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_released = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    platform_fee_collected = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    released_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Escrow Account'
        verbose_name_plural = 'Escrow Accounts'
    
    def __str__(self):
        return f"{self.project.title} - {self.status} (R{self.total_held})"
    
    @property
    def pending_amount(self):
        """Amount still held in escrow"""
        return self.total_held - self.total_released

