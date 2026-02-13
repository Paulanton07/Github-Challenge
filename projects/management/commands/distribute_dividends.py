from django.core.management.base import BaseCommand
from projects.models import Project
from decimal import Decimal


class Command(BaseCommand):
    help = 'Distribute dividends for a project'

    def add_arguments(self, parser):
        parser.add_argument('project_id', type=int, help='ID of the project')
        parser.add_argument(
            '--amount',
            type=float,
            help='Specific revenue amount to distribute (defaults to all pending revenue)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be distributed without creating records'
        )

    def handle(self, *args, **options):
        project_id = options['project_id']
        amount = Decimal(str(options['amount'])) if options['amount'] else None
        dry_run = options['dry_run']

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Project with ID {project_id} not found'))
            return

        self.stdout.write(self.style.SUCCESS(f'\nProject: {project.title}'))
        self.stdout.write(f'Total Revenue: R{project.total_revenue}')
        self.stdout.write(f'Already Distributed: R{project.revenue_distributed}')
        self.stdout.write(f'Pending Revenue: R{project.pending_revenue}')
        
        # Calculate dividends
        dividends = project.calculate_dividends(amount)
        
        if not dividends:
            self.stdout.write(self.style.WARNING('\nNo dividends to distribute'))
            return
        
        summary = dividends.get('_summary', {})
        
        self.stdout.write(self.style.SUCCESS(f'\n--- Dividend Distribution Preview ---'))
        self.stdout.write(f"Revenue Pool: R{summary.get('revenue_pool', 0)}")
        self.stdout.write(f"Investors: {summary.get('investors_count', 0)}\n")
        
        # Remove summary for display
        dividends.pop('_summary', None)
        
        for username, data in dividends.items():
            self.stdout.write(
                f"  {username}: R{data['dividend']} ({data['ownership']}% of R{data['investment_amount']})"
            )
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\n[DRY RUN] No records created'))
        else:
            # Actually distribute
            payments = project.distribute_dividends(amount)
            self.stdout.write(self.style.SUCCESS(f'\n✓ Created {len(payments)} dividend payment records'))
            self.stdout.write(f'Updated revenue_distributed to R{project.revenue_distributed}')
