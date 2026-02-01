from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'status', 'funding_goal', 'current_funding', 'funding_percentage', 'total_investors', 'end_date']
    list_filter = ['status', 'created_at', 'end_date']
    search_fields = ['title', 'description', 'creator__username']
    readonly_fields = ['current_funding', 'funding_percentage', 'total_investors', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('creator', 'title', 'description', 'image', 'status')
        }),
        ('Funding Details', {
            'fields': ('funding_goal', 'current_funding', 'funding_percentage', 'total_investors')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date')
        }),
        ('Revenue & Dividends', {
            'fields': ('total_revenue', 'revenue_distributed')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['calculate_project_dividends']
    
    def funding_percentage(self, obj):
        return f"{obj.funding_percentage:.2f}%"
    funding_percentage.short_description = 'Funding %'
    
    def total_investors(self, obj):
        return obj.total_investors
    total_investors.short_description = 'Investors'
    
    def calculate_project_dividends(self, request, queryset):
        for project in queryset:
            dividends = project.calculate_dividends()
            self.message_user(request, f"Dividends calculated for '{project.title}': {dividends}")
    calculate_project_dividends.short_description = "Calculate dividends for selected projects"

