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
    
    def calculate_dividends(self):
        """Calculate pending dividends for all investors"""
        if self.total_revenue <= 0 or self.current_funding <= 0:
            return {}
        
        pending_revenue = self.total_revenue - self.revenue_distributed
        dividends = {}
        
        for investment in self.investments.all():
            ownership_percentage = (investment.amount / self.current_funding) * 100
            dividend_amount = (ownership_percentage / 100) * pending_revenue
            dividends[investment.investor.username] = {
                'ownership': ownership_percentage,
                'dividend': dividend_amount
            }
        
        return dividends

