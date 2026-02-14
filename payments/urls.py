from django.urls import path
from . import views

urlpatterns = [
    # Stripe Connect for project creators
    path('connect/', views.connect_stripe_account, name='connect_stripe_account'),
    path('connect/refresh/', views.stripe_connect_refresh, name='stripe_connect_refresh'),
    path('connect/return/', views.stripe_connect_return, name='stripe_connect_return'),
    
    # Investment payments
    path('invest/<int:project_id>/', views.make_investment_payment, name='make_investment_payment'),
    path('success/<int:investment_id>/', views.investment_success, name='investment_success'),
    
    # Payment history
    path('history/', views.payment_history, name='payment_history'),
    
    # Stripe webhooks
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]
