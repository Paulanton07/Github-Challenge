from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from .models import Investment, DividendPayment

@login_required
def investment_portfolio(request):
    investments = Investment.objects.filter(
        investor=request.user,
        status='completed'
    ).select_related('project')
    
    # Calculate portfolio statistics
    total_invested = investments.aggregate(Sum('amount'))['amount__sum'] or 0
    total_dividends = DividendPayment.objects.filter(
        investment__investor=request.user,
        status='paid'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    pending_dividends = DividendPayment.objects.filter(
        investment__investor=request.user,
        status='pending'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    portfolio_data = []
    for inv in investments:
        portfolio_data.append({
            'investment': inv,
            'project': inv.project,
            'ownership': round(inv.ownership_percentage, 2),
            'dividends_earned': inv.total_dividends_earned,
            'paid_dividends': inv.paid_dividends,
            'pending_dividends': inv.pending_dividends,
            'potential_return': inv.calculate_potential_dividend(inv.project.pending_revenue),
        })
    
    context = {
        'portfolio_data': portfolio_data,
        'total_invested': total_invested,
        'total_dividends': total_dividends,
        'pending_dividends': pending_dividends,
        'total_return': total_dividends + pending_dividends,
        'roi_percentage': round((total_dividends / total_invested * 100), 2) if total_invested > 0 else 0,
    }
    return render(request, 'investments/portfolio.html', context)

@login_required
def dividend_history(request):
    investments = Investment.objects.filter(investor=request.user)
    dividends = DividendPayment.objects.filter(
        investment__in=investments
    ).select_related('investment__project').order_by('-calculated_at')
    
    # Group by status
    paid_dividends = dividends.filter(status='paid')
    pending_dividends = dividends.filter(status='pending')
    failed_dividends = dividends.filter(status='failed')
    
    context = {
        'dividends': dividends,
        'paid_dividends': paid_dividends,
        'pending_dividends': pending_dividends,
        'failed_dividends': failed_dividends,
    }
    return render(request, 'investments/dividend_history.html', context)

@login_required
def investment_analytics(request):
    """Detailed analytics and visualizations for investor"""
    investments = Investment.objects.filter(
        investor=request.user,
        status='completed'
    ).select_related('project')
    
    # Per-project breakdown
    project_breakdown = []
    for inv in investments:
        project_breakdown.append({
            'project_name': inv.project.title,
            'invested': inv.amount,
            'ownership': round(inv.ownership_percentage, 2),
            'total_dividends': inv.total_dividends_earned,
            'paid': inv.paid_dividends,
            'pending': inv.pending_dividends,
            'roi': round((inv.total_dividends_earned / inv.amount * 100), 2) if inv.amount > 0 else 0,
        })
    
    # Overall stats
    total_invested = sum(p['invested'] for p in project_breakdown)
    total_dividends = sum(p['total_dividends'] for p in project_breakdown)
    
    context = {
        'project_breakdown': project_breakdown,
        'total_invested': total_invested,
        'total_dividends': total_dividends,
        'overall_roi': round((total_dividends / total_invested * 100), 2) if total_invested > 0 else 0,
        'project_count': len(project_breakdown),
    }
    return render(request, 'investments/analytics.html', context)

