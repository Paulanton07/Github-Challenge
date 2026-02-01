from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserStorefront, StorefrontSection

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_verified', 'total_invested', 'total_projects_backed']
    list_filter = ['is_verified', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('bio', 'profile_picture', 'phone_number', 'date_of_birth')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verification_date')
        }),
    )
    
    readonly_fields = ['total_invested', 'total_projects_backed', 'created_at', 'updated_at']
    
    def total_invested(self, obj):
        return f"R{obj.total_invested}"
    total_invested.short_description = 'Total Invested'
    
    def total_projects_backed(self, obj):
        return obj.total_projects_backed
    total_projects_backed.short_description = 'Projects Backed'


@admin.register(UserStorefront)
class UserStorefrontAdmin(admin.ModelAdmin):
    list_display = ['user', 'storefront_name', 'slug', 'template', 'is_active', 'created_at']
    list_filter = ['template', 'is_active', 'created_at']
    search_fields = ['user__username', 'storefront_name', 'slug']
    prepopulated_fields = {'slug': ('storefront_name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'storefront_name', 'slug', 'tagline', 'about_text', 'is_active')
        }),
        ('Branding', {
            'fields': ('logo', 'banner_image', 'favicon')
        }),
        ('Design', {
            'fields': ('template', 'primary_color', 'secondary_color', 'accent_color', 'background_color', 'text_color')
        }),
        ('Advanced Customization', {
            'fields': ('custom_css', 'custom_html_header', 'custom_html_footer'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url')
        }),
        ('Contact', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Settings', {
            'fields': ('show_featured_projects', 'projects_per_page')
        }),
    )


@admin.register(StorefrontSection)
class StorefrontSectionAdmin(admin.ModelAdmin):
    list_display = ['storefront', 'section_type', 'title', 'order', 'is_visible']
    list_filter = ['section_type', 'is_visible']
    search_fields = ['storefront__user__username', 'title']
    list_editable = ['order', 'is_visible']

