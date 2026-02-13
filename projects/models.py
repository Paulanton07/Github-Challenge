from django.db import models
from django.conf import settings
from django.utils import timezone

class Project(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('funded', 'Funded'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    
    funding_goal = models.DecimalField(max_digits=12, decimal_places=2)
    current_funding = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    
    # Revenue tracking for dividend calculation
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    revenue_distributed = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def funding_percentage(self):
        if self.funding_goal > 0:
            return (self.current_funding / self.funding_goal) * 100
        return 0
    
    @property
    def is_active(self):
        return self.status == 'active' and self.end_date > timezone.now()
    
    @property
    def total_investors(self):
        return self.investments.values('investor').distinct().count()
    
    @property
    def pending_revenue(self):
        """Revenue not yet distributed as dividends"""
        return self.total_revenue - self.revenue_distributed
    
    @property
    def dividend_pool(self):
        """Total amount available for dividend distribution"""
        return self.pending_revenue
    
    def calculate_dividends(self, revenue_amount=None):
        """
        Calculate dividends for all investors based on ownership percentage.
        
        Args:
            revenue_amount: Specific revenue to distribute. If None, uses all pending revenue.
        
        Returns:
            dict: Investor data with ownership and calculated dividends
        """
        if self.current_funding <= 0:
            return {}
        
        # Use specified amount or all pending revenue
        distributable_revenue = revenue_amount if revenue_amount else self.pending_revenue
        
        if distributable_revenue <= 0:
            return {}
        
        dividends = {}
        total_dividend_paid = 0
        investors_count = 0
        
        # Get completed investments only
        completed_investments = self.investments.filter(status='completed')
        
        for investment in completed_investments:
            ownership_percentage = (investment.amount / self.current_funding) * 100
            dividend_amount = (ownership_percentage / 100) * distributable_revenue
            
            dividends[investment.investor.username] = {
                'investment_id': investment.id,
                'investment_amount': float(investment.amount),
                'ownership': round(ownership_percentage, 2),
                'dividend': round(dividend_amount, 2)
            }
            total_dividend_paid += dividend_amount
            investors_count += 1
        
        # Add summary
        dividends['_summary'] = {
            'total_distributed': round(total_dividend_paid, 2),
            'revenue_pool': float(distributable_revenue),
            'investors_count': investors_count
        }
        
        return dividends
    
    def distribute_dividends(self, revenue_amount=None):
        """
        Create dividend payment records for all investors.
        
        Args:
            revenue_amount: Specific revenue to distribute. If None, uses all pending revenue.
        
        Returns:
            list: Created DividendPayment objects
        """
        from investments.models import DividendPayment
        
        dividends_data = self.calculate_dividends(revenue_amount)
        
        if not dividends_data or '_summary' not in dividends_data:
            return []
        
        # Remove summary for processing
        summary = dividends_data.pop('_summary')
        dividend_payments = []
        
        for username, data in dividends_data.items():
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            try:
                investment = self.investments.get(id=data['investment_id'])
                
                # Create dividend payment record
                dividend = DividendPayment.objects.create(
                    investment=investment,
                    amount=data['dividend'],
                    status='pending',
                    notes=f"Dividend from {summary['revenue_pool']} revenue. {data['ownership']}% ownership."
                )
                dividend_payments.append(dividend)
                
            except Exception as e:
                continue
        
        # Update revenue distributed
        if dividend_payments:
            distributed_amount = revenue_amount if revenue_amount else self.pending_revenue
            self.revenue_distributed += distributed_amount
            self.save()
        
        return dividend_payments

