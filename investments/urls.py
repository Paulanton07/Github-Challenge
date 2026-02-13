from django.urls import path
from . import views

urlpatterns = [
    path('portfolio/', views.investment_portfolio, name='investment_portfolio'),
    path('dividends/', views.dividend_history, name='dividend_history'),
    path('analytics/', views.investment_analytics, name='investment_analytics'),
]
