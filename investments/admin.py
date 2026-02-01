from django.contrib import admin
from .models import Investment, DividendPayment

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['investor', 'project', 'amount', 'ownership_percentage', 'status', 'invested_at']
    list_filter = ['status', 'invested_at']
    search_fields = ['investor__username', 'project__title', 'payment_reference']
    readonly_fields = ['ownership_percentage', 'total_dividends_earned', 'invested_at', 'updated_at']
    
    fieldsets = (
        ('Investment Details', {
            'fields': ('investor', 'project', 'amount', 'status')
        }),
        ('Payment Information', {
            'fields': ('payment_reference',)
        }),
        ('Ownership & Returns', {
            'fields': ('ownership_percentage', 'total_dividends_earned')
        }),
        ('Timestamps', {
            'fields': ('invested_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def ownership_percentage(self, obj):
        return f"{obj.ownership_percentage:.4f}%"
    ownership_percentage.short_description = 'Ownership %'
    
    def total_dividends_earned(self, obj):
        return f"R{obj.total_dividends_earned}"
    total_dividends_earned.short_description = 'Total Dividends'


@admin.register(DividendPayment)
class DividendPaymentAdmin(admin.ModelAdmin):
    list_display = ['investment', 'amount', 'status', 'calculated_at', 'paid_at']
    list_filter = ['status', 'calculated_at', 'paid_at']
    search_fields = ['investment__investor__username', 'investment__project__title', 'payment_reference']
    readonly_fields = ['calculated_at']
    
    fieldsets = (
        ('Dividend Information', {
            'fields': ('investment', 'amount', 'status')
        }),
        ('Payment Details', {
            'fields': ('payment_reference', 'paid_at', 'notes')
        }),
        ('Timestamps', {
            'fields': ('calculated_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_paid']
    
    def mark_as_paid(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='paid', paid_at=timezone.now())
        self.message_user(request, f"{updated} dividend payment(s) marked as paid.")
    mark_as_paid.short_description = "Mark selected dividends as paid"

