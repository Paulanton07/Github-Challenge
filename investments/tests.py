from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from projects.models import Project
from investments.models import Investment, DividendPayment

User = get_user_model()


class DividendCalculationTests(TestCase):
    def setUp(self):
        # Create users
        self.creator = User.objects.create_user(username='creator', password='test123')
        self.investor1 = User.objects.create_user(username='investor1', password='test123')
        self.investor2 = User.objects.create_user(username='investor2', password='test123')
        self.investor3 = User.objects.create_user(username='investor3', password='test123')
        
        # Create project
        self.project = Project.objects.create(
            creator=self.creator,
            title='Test Workshop Bench',
            description='Building a bench',
            funding_goal=Decimal('3000.00'),
            current_funding=Decimal('3000.00'),
            status='funded',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            total_revenue=Decimal('1000.00'),
            revenue_distributed=Decimal('0.00')
        )
        
        # Create investments matching README example
        self.inv1 = Investment.objects.create(
            investor=self.investor1,
            project=self.project,
            amount=Decimal('1500.00'),  # 50% ownership
            status='completed'
        )
        
        self.inv2 = Investment.objects.create(
            investor=self.investor2,
            project=self.project,
            amount=Decimal('900.00'),  # 30% ownership
            status='completed'
        )
        
        self.inv3 = Investment.objects.create(
            investor=self.investor3,
            project=self.project,
            amount=Decimal('600.00'),  # 20% ownership
            status='completed'
        )
    
    def test_ownership_percentage_calculation(self):
        """Test ownership percentages match README example"""
        self.assertEqual(round(self.inv1.ownership_percentage, 0), 50)
        self.assertEqual(round(self.inv2.ownership_percentage, 0), 30)
        self.assertEqual(round(self.inv3.ownership_percentage, 0), 20)
    
    def test_dividend_calculation(self):
        """Test dividend distribution matches README example (R1000 profit)"""
        dividends = self.project.calculate_dividends()
        
        # Check investor1 (50% ownership should get R500)
        self.assertEqual(round(dividends['investor1']['dividend'], 0), 500)
        
        # Check investor2 (30% ownership should get R300)
        self.assertEqual(round(dividends['investor2']['dividend'], 0), 300)
        
        # Check investor3 (20% ownership should get R200)
        self.assertEqual(round(dividends['investor3']['dividend'], 0), 200)
    
    def test_pending_revenue(self):
        """Test pending revenue calculation"""
        self.assertEqual(self.project.pending_revenue, Decimal('1000.00'))
        
        # After distributing some revenue
        self.project.revenue_distributed = Decimal('400.00')
        self.assertEqual(self.project.pending_revenue, Decimal('600.00'))
    
    def test_distribute_dividends_creates_records(self):
        """Test that distribute_dividends creates DividendPayment records"""
        payments = self.project.distribute_dividends()
        
        self.assertEqual(len(payments), 3)
        self.assertEqual(DividendPayment.objects.count(), 3)
        
        # Check revenue was marked as distributed
        self.project.refresh_from_db()
        self.assertEqual(self.project.revenue_distributed, Decimal('1000.00'))
    
    def test_distribute_partial_dividends(self):
        """Test distributing only partial revenue"""
        payments = self.project.distribute_dividends(Decimal('500.00'))
        
        self.assertEqual(len(payments), 3)
        
        # investor1 should get 50% of R500 = R250
        inv1_payment = DividendPayment.objects.get(investment=self.inv1)
        self.assertEqual(round(inv1_payment.amount, 0), 250)
        
        # Check only partial revenue marked as distributed
        self.project.refresh_from_db()
        self.assertEqual(self.project.revenue_distributed, Decimal('500.00'))
        self.assertEqual(self.project.pending_revenue, Decimal('500.00'))
    
    def test_only_completed_investments_get_dividends(self):
        """Test that only completed investments receive dividends"""
        # Add a pending investment (same investor as inv1 but pending)
        pending_inv = Investment.objects.create(
            investor=User.objects.create_user(username='pending_investor', password='test123'),
            project=self.project,
            amount=Decimal('1000.00'),
            status='pending'
        )
        
        dividends = self.project.calculate_dividends()
        
        # Should still only have 3 investors in dividend calculation (not 4)
        self.assertEqual(dividends['_summary']['investors_count'], 3)
    
    def test_investment_dividend_tracking(self):
        """Test investment-level dividend tracking"""
        # Create some dividend payments
        div1 = DividendPayment.objects.create(
            investment=self.inv1,
            amount=Decimal('100.00'),
            status='paid'
        )
        
        div2 = DividendPayment.objects.create(
            investment=self.inv1,
            amount=Decimal('50.00'),
            status='pending'
        )
        
        self.assertEqual(self.inv1.total_dividends_earned, Decimal('150.00'))
        self.assertEqual(self.inv1.paid_dividends, Decimal('100.00'))
        self.assertEqual(self.inv1.pending_dividends, Decimal('50.00'))
    
    def test_potential_dividend_calculation(self):
        """Test calculating potential dividends from hypothetical revenue"""
        # investor1 has 50% ownership
        potential = self.inv1.calculate_potential_dividend(Decimal('2000.00'))
        self.assertEqual(round(potential, 0), 1000)  # 50% of R2000
        
        # investor2 has 30% ownership
        potential = self.inv2.calculate_potential_dividend(Decimal('2000.00'))
        self.assertEqual(round(potential, 0), 600)  # 30% of R2000


class ProjectModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.project = Project.objects.create(
            creator=self.user,
            title='Test Project',
            description='Test description',
            funding_goal=Decimal('5000.00'),
            current_funding=Decimal('2500.00'),
            status='active',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30)
        )
    
    def test_funding_percentage(self):
        """Test funding percentage calculation"""
        self.assertEqual(self.project.funding_percentage, 50.0)
    
    def test_is_active(self):
        """Test is_active property"""
        self.assertTrue(self.project.is_active)
        
        # Change status
        self.project.status = 'completed'
        self.assertFalse(self.project.is_active)
    
    def test_total_investors(self):
        """Test investor count"""
        investor1 = User.objects.create_user(username='inv1', password='test123')
        investor2 = User.objects.create_user(username='inv2', password='test123')
        
        Investment.objects.create(
            investor=investor1,
            project=self.project,
            amount=Decimal('1000.00'),
            status='completed'
        )
        
        Investment.objects.create(
            investor=investor2,
            project=self.project,
            amount=Decimal('1500.00'),
            status='completed'
        )
        
        self.assertEqual(self.project.total_investors, 2)

