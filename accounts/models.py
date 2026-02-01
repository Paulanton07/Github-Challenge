from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Financial settings (for future payment integration)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    @property
    def total_invested(self):
        return sum(inv.amount for inv in self.investments.all())
    
    @property
    def total_projects_backed(self):
        return self.investments.values('project').distinct().count()


class UserStorefront(models.Model):
    TEMPLATE_CHOICES = [
        ('modern', 'Modern & Clean'),
        ('bold', 'Bold & Colorful'),
        ('minimal', 'Minimal & Professional'),
        ('creative', 'Creative & Artistic'),
    ]
    
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='storefront')
    
    # Basic Settings
    storefront_name = models.CharField(max_length=200, default='My Crowdfund Store')
    slug = models.SlugField(unique=True, max_length=100)
    tagline = models.CharField(max_length=255, blank=True)
    about_text = models.TextField(blank=True)
    
    # Branding
    logo = models.ImageField(upload_to='storefronts/logos/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='storefronts/banners/', blank=True, null=True)
    favicon = models.ImageField(upload_to='storefronts/favicons/', blank=True, null=True)
    
    # Design Customization
    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='modern')
    primary_color = models.CharField(max_length=7, default='#3498db')
    secondary_color = models.CharField(max_length=7, default='#2c3e50')
    accent_color = models.CharField(max_length=7, default='#27ae60')
    background_color = models.CharField(max_length=7, default='#ffffff')
    text_color = models.CharField(max_length=7, default='#333333')
    
    # Advanced - Custom Code
    custom_css = models.TextField(blank=True, help_text='Custom CSS code')
    custom_html_header = models.TextField(blank=True, help_text='Custom HTML for header section')
    custom_html_footer = models.TextField(blank=True, help_text='Custom HTML for footer section')
    
    # Social Links
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # Contact
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    show_featured_projects = models.BooleanField(default=True)
    projects_per_page = models.IntegerField(default=6)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Storefront"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f'/store/{self.slug}/'


class StorefrontSection(models.Model):
    SECTION_TYPES = [
        ('hero', 'Hero Banner'),
        ('about', 'About Section'),
        ('projects', 'Projects Grid'),
        ('stats', 'Statistics'),
        ('testimonials', 'Testimonials'),
        ('contact', 'Contact Form'),
        ('custom', 'Custom HTML'),
    ]
    
    storefront = models.ForeignKey(UserStorefront, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.storefront.user.username} - {self.get_section_type_display()}"

