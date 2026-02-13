from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'status', 'funding_display', 'funding_percentage_display', 'total_investors', 'revenue_display', 'end_date']
    list_filter = ['status', 'created_at', 'end_date']
    search_fields = ['title', 'description', 'creator__username']
    readonly_fields = ['current_funding', 'funding_percentage_display', 'total_investors', 'pending_revenue_display', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('creator', 'title', 'description', 'image', 'status')
        }),
        ('Funding Details', {
            'fields': ('funding_goal', 'current_funding', 'funding_percentage_display', 'total_investors')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date')
        }),
        ('Revenue & Dividends', {
            'fields': ('total_revenue', 'revenue_distributed', 'pending_revenue_display'),
            'description': 'Track revenue and manage dividend distributions'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['preview_dividends', 'distribute_all_pending']
    
    def funding_display(self, obj):
        return format_html(
            '<strong>R{:,.2f}</strong> / R{:,.2f}',
            obj.current_funding,
            obj.funding_goal
        )
    funding_display.short_description = 'Funding'
    
    def funding_percentage_display(self, obj):
        percentage = obj.funding_percentage
        color = 'green' if percentage >= 100 else 'orange' if percentage >= 50 else 'red'
        return format_html(
            '<span style="color: {};">{:.2f}%</span>',
            color,
            percentage
        )
    funding_percentage_display.short_description = 'Progress'
    
    def revenue_display(self, obj):
        return format_html(
            'R{:,.2f}<br><small>Pending: R{:,.2f}</small>',
            obj.total_revenue,
            obj.pending_revenue
        )
    revenue_display.short_description = 'Revenue'
    
    def pending_revenue_display(self, obj):
        return f"R{obj.pending_revenue:,.2f}"
    pending_revenue_display.short_description = 'Pending Revenue'
    
    def preview_dividends(self, request, queryset):
        for project in queryset:
            dividends = project.calculate_dividends()
            if dividends and '_summary' in dividends:
                summary = dividends['_summary']
                self.message_user(
                    request,
                    f"{project.title}: R{summary['revenue_pool']} to distribute among {summary['investors_count']} investors"
                )
            else:
                self.message_user(request, f"{project.title}: No dividends to distribute", level='warning')
    preview_dividends.short_description = "Preview dividend distribution"
    
    def distribute_all_pending(self, request, queryset):
        total_payments = 0
        for project in queryset:
            if project.pending_revenue > 0:
                payments = project.distribute_dividends()
                total_payments += len(payments)
                self.message_user(
                    request,
                    f"{project.title}: Created {len(payments)} dividend payments"
                )
            else:
                self.message_user(
                    request,
                    f"{project.title}: No pending revenue to distribute",
                    level='warning'
                )
        if total_payments > 0:
            self.message_user(request, f"Total: {total_payments} dividend payment records created")
    distribute_all_pending.short_description = "Distribute all pending revenue"


