from django.db import models
from django.conf import settings
from django.utils import timezone

class Investment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    investor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='investments')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='investments')
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Mock payment reference (will be replaced with real payment ID later)
    payment_reference = models.CharField(max_length=100, blank=True)
    
    invested_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-invested_at']
    
    def __str__(self):
        return f"{self.investor.username} - {self.project.title} - R{self.amount}"
    
    @property
    def ownership_percentage(self):
        if self.project.current_funding > 0:
            return (self.amount / self.project.current_funding) * 100
        return 0
    
    @property
    def total_dividends_earned(self):
        """Total dividends earned across all statuses"""
        return sum(div.amount for div in self.dividend_payments.all())
    
    @property
    def paid_dividends(self):
        """Total dividends that have been paid out"""
        return sum(div.amount for div in self.dividend_payments.filter(status='paid'))
    
    @property
    def pending_dividends(self):
        """Total dividends pending payment"""
        return sum(div.amount for div in self.dividend_payments.filter(status='pending'))
    
    def calculate_potential_dividend(self, revenue_amount):
        """
        Calculate potential dividend from a hypothetical revenue amount.
        
        Args:
            revenue_amount: The revenue amount to calculate dividend from
        
        Returns:
            Decimal: Calculated dividend amount
        """
        if self.project.current_funding > 0:
            ownership = self.ownership_percentage / 100
            return revenue_amount * ownership
        return 0


class DividendPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, related_name='dividend_payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Mock payment reference (will be replaced with real payout ID later)
    payment_reference = models.CharField(max_length=100, blank=True)
    
    calculated_at = models.DateTimeField(default=timezone.now)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-calculated_at']
    
    def __str__(self):
        return f"Dividend: R{self.amount} to {self.investment.investor.username}"

