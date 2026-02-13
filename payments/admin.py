from django.contrib import admin
from django.utils.html import format_html
from .models import PaymentAccount, StripeCustomer, PaymentTransaction, EscrowAccount


@admin.register(PaymentAccount)
class PaymentAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'stripe_account_id', 'account_type', 'onboarding_complete', 'charges_enabled', 'payouts_enabled', 'created_at']
    list_filter = ['account_type', 'onboarding_complete', 'charges_enabled', 'payouts_enabled']
    search_fields = ['user__username', 'stripe_account_id']
    readonly_fields = ['stripe_account_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Account Information', {
            'fields': ('user', 'stripe_account_id', 'account_type')
        }),
        ('Status', {
            'fields': ('onboarding_complete', 'charges_enabled', 'payouts_enabled', 'capabilities_enabled')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'stripe_customer_id', 'default_payment_method', 'created_at']
    search_fields = ['user__username', 'stripe_customer_id']
    readonly_fields = ['stripe_customer_id', 'created_at', 'updated_at']


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id_display', 'user', 'transaction_type', 'amount_display', 'status', 'created_at']
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['transaction_id', 'user__username']
    readonly_fields = ['transaction_id', 'processor_response', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('transaction_id', 'user', 'investment', 'transaction_type', 'status')
        }),
        ('Amount', {
            'fields': ('amount', 'currency')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'error_message')
        }),
        ('Processor Data', {
            'fields': ('processor_response',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def transaction_id_display(self, obj):
        return obj.transaction_id[:20] + '...' if len(obj.transaction_id) > 20 else obj.transaction_id
    transaction_id_display.short_description = 'Transaction ID'
    
    def amount_display(self, obj):
        color = 'green' if obj.status == 'succeeded' else 'orange' if obj.status == 'pending' else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">R{:,.2f}</span>',
            color,
            obj.amount
        )
    amount_display.short_description = 'Amount'


@admin.register(EscrowAccount)
class EscrowAccountAdmin(admin.ModelAdmin):
    list_display = ['project', 'status', 'total_held_display', 'total_released_display', 'platform_fee_display', 'pending_display']
    list_filter = ['status', 'created_at']
    search_fields = ['project__title']
    readonly_fields = ['created_at', 'updated_at', 'pending_display']
    
    fieldsets = (
        ('Project', {
            'fields': ('project', 'status')
        }),
        ('Funds', {
            'fields': ('total_held', 'total_released', 'platform_fee_collected', 'pending_display')
        }),
        ('Payment References', {
            'fields': ('stripe_payment_intent_ids',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('released_at', 'refunded_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def total_held_display(self, obj):
        return format_html('<strong>R{:,.2f}</strong>', obj.total_held)
    total_held_display.short_description = 'Total Held'
    
    def total_released_display(self, obj):
        color = 'green' if obj.total_released > 0 else 'gray'
        return format_html(
            '<span style="color: {};">R{:,.2f}</span>',
            color,
            obj.total_released
        )
    total_released_display.short_description = 'Released'
    
    def platform_fee_display(self, obj):
        return format_html('R{:,.2f}', obj.platform_fee_collected)
    platform_fee_display.short_description = 'Platform Fee'
    
    def pending_display(self, obj):
        pending = obj.pending_amount
        return format_html(
            '<span style="color: orange; font-weight: bold;">R{:,.2f}</span>',
            pending
        )
    pending_display.short_description = 'Pending in Escrow'

