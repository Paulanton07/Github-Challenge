from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Investment, DividendPayment

@login_required
def investment_portfolio(request):
    investments = Investment.objects.filter(
        investor=request.user,
        status='completed'
    ).select_related('project')
    
    portfolio_data = []
    for inv in investments:
        portfolio_data.append({
            'investment': inv,
            'project': inv.project,
            'ownership': inv.ownership_percentage,
            'dividends_earned': inv.total_dividends_earned,
        })
    
    context = {
        'portfolio_data': portfolio_data,
    }
    return render(request, 'investments/portfolio.html', context)

@login_required
def dividend_history(request):
    investments = Investment.objects.filter(investor=request.user)
    dividends = DividendPayment.objects.filter(
        investment__in=investments
    ).order_by('-calculated_at')
    
    context = {
        'dividends': dividends,
    }
    return render(request, 'investments/dividend_history.html', context)

