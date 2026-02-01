from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from projects.models import Project
from investments.models import Investment, DividendPayment
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        # Create sample users
        users = []
        for i in range(1, 6):
            user, created = User.objects.get_or_create(
                username=f'investor{i}',
                defaults={
                    'email': f'investor{i}@example.com',
                    'first_name': f'Investor',
                    'last_name': f'#{i}',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))
        
        # Create sample projects
        admin = User.objects.get(username='admin')
        
        projects_data = [
            {
                'title': 'Handcrafted Wooden Bench',
                'description': 'Build a beautiful handcrafted wooden bench for the community park. Materials include oak wood, varnish, and hardware. This bench will serve the community for years to come.',
                'funding_goal': Decimal('3000.00'),
                'end_date': timezone.now() + timedelta(days=30),
            },
            {
                'title': 'Mobile App for Local Farmers',
                'description': 'Develop a mobile application to connect local farmers directly with consumers. This will help farmers get better prices and consumers get fresher produce.',
                'funding_goal': Decimal('15000.00'),
                'end_date': timezone.now() + timedelta(days=45),
            },
            {
                'title': 'Community Garden Project',
                'description': 'Establish a community garden where residents can grow their own vegetables. Includes seeds, tools, irrigation system, and garden plots for 20 families.',
                'funding_goal': Decimal('8000.00'),
                'end_date': timezone.now() + timedelta(days=60),
            },
            {
                'title': 'Small Bakery Equipment',
                'description': 'Purchase professional baking equipment for a new small bakery. Equipment includes commercial oven, mixer, refrigeration unit, and display cases.',
                'funding_goal': Decimal('25000.00'),
                'end_date': timezone.now() + timedelta(days=20),
            },
        ]
        
        projects = []
        for data in projects_data:
            project, created = Project.objects.get_or_create(
                title=data['title'],
                defaults={
                    'creator': admin,
                    'description': data['description'],
                    'funding_goal': data['funding_goal'],
                    'end_date': data['end_date'],
                    'status': 'active',
                }
            )
            projects.append(project)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(projects)} projects'))
        
        # Create sample investments
        investment_count = 0
        for project in projects[:3]:  # Invest in first 3 projects
            for user in users[:3]:  # First 3 users invest
                amount = Decimal('500.00') + (Decimal('100.00') * investment_count)
                investment, created = Investment.objects.get_or_create(
                    investor=user,
                    project=project,
                    defaults={
                        'amount': amount,
                        'status': 'completed',
                        'payment_reference': f'MOCK-{investment_count:06d}'
                    }
                )
                if created:
                    project.current_funding += amount
                    investment_count += 1
            
            project.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {investment_count} investments'))
        
        # Add sample revenue and dividends for first project
        first_project = projects[0]
        first_project.total_revenue = Decimal('5000.00')
        first_project.save()
        
        # Calculate and create dividend payments
        dividends = first_project.calculate_dividends()
        dividend_count = 0
        for username, data in dividends.items():
            user = User.objects.get(username=username)
            for investment in first_project.investments.filter(investor=user):
                DividendPayment.objects.get_or_create(
                    investment=investment,
                    defaults={
                        'amount': Decimal(str(data['dividend'])),
                        'status': 'paid',
                        'paid_at': timezone.now(),
                        'payment_reference': f'DIV-{dividend_count:06d}'
                    }
                )
                dividend_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {dividend_count} dividend payments'))
        self.stdout.write(self.style.SUCCESS('Sample data population complete!'))
