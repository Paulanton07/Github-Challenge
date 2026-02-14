from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from projects.models import Project
from investments.models import Investment
from .models import UserStorefront, StorefrontSection

def home(request):
    active_projects = Project.objects.filter(status='active').order_by('-created_at')[:6]
    context = {
        'active_projects': active_projects,
        'total_projects': Project.objects.count(),
        'total_funded': Project.objects.filter(status='funded').count(),
    }
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    user_investments = Investment.objects.filter(investor=request.user, status='completed')
    user_projects = Project.objects.filter(creator=request.user)
    
    total_invested = user_investments.aggregate(Sum('amount'))['amount__sum'] or 0
    total_dividends = sum(inv.total_dividends_earned for inv in user_investments)
    
    # Chart data: Portfolio distribution
    portfolio_labels = []
    portfolio_amounts = []
    for inv in user_investments:
        portfolio_labels.append(inv.project.title[:20])
        portfolio_amounts.append(float(inv.amount))
    
    # Chart data: Project funding progress
    project_names = []
    project_progress = []
    project_goals = []
    for proj in user_projects[:5]:
        project_names.append(proj.title[:15])
        project_progress.append(float(proj.current_funding))
        project_goals.append(float(proj.funding_goal))
    
    context = {
        'user_investments': user_investments,
        'user_projects': user_projects,
        'total_invested': total_invested,
        'total_dividends': total_dividends,
        'projects_backed': user_investments.values('project').distinct().count(),
        'portfolio_labels': portfolio_labels,
        'portfolio_amounts': portfolio_amounts,
        'project_names': project_names,
        'project_progress': project_progress,
        'project_goals': project_goals,
    }
    return render(request, 'dashboard.html', context)

def storefront_view(request, slug):
    storefront = get_object_or_404(UserStorefront, slug=slug, is_active=True)
    projects = Project.objects.filter(
        creator=storefront.user,
        status__in=['active', 'funded']
    ).order_by('-created_at')[:storefront.projects_per_page]
    
    context = {
        'storefront': storefront,
        'projects': projects,
        'sections': storefront.sections.filter(is_visible=True),
    }
    return render(request, 'storefront/storefront_view.html', context)

@login_required
def storefront_builder(request):
    storefront, created = UserStorefront.objects.get_or_create(
        user=request.user,
        defaults={'storefront_name': f"{request.user.username}'s Store"}
    )
    
    if request.method == 'POST':
        # Basic settings
        storefront.storefront_name = request.POST.get('storefront_name', storefront.storefront_name)
        storefront.tagline = request.POST.get('tagline', '')
        storefront.about_text = request.POST.get('about_text', '')
        
        # Design
        storefront.template = request.POST.get('template', 'modern')
        storefront.primary_color = request.POST.get('primary_color', '#3498db')
        storefront.secondary_color = request.POST.get('secondary_color', '#2c3e50')
        storefront.accent_color = request.POST.get('accent_color', '#27ae60')
        
        # Advanced code
        storefront.custom_css = request.POST.get('custom_css', '')
        storefront.custom_html_header = request.POST.get('custom_html_header', '')
        storefront.custom_html_footer = request.POST.get('custom_html_footer', '')
        
        # Social links
        storefront.facebook_url = request.POST.get('facebook_url', '')
        storefront.twitter_url = request.POST.get('twitter_url', '')
        storefront.instagram_url = request.POST.get('instagram_url', '')
        storefront.linkedin_url = request.POST.get('linkedin_url', '')
        
        # Contact
        storefront.contact_email = request.POST.get('contact_email', '')
        storefront.contact_phone = request.POST.get('contact_phone', '')
        
        # File uploads
        if 'logo' in request.FILES:
            storefront.logo = request.FILES['logo']
        if 'banner_image' in request.FILES:
            storefront.banner_image = request.FILES['banner_image']
        
        storefront.save()
        messages.success(request, 'Storefront updated successfully!')
        return redirect('storefront_builder')
    
    context = {
        'storefront': storefront,
    }
    return render(request, 'storefront/builder.html', context)


