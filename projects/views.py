from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Project
from investments.models import Investment
import uuid

def project_list(request):
    projects = Project.objects.filter(status='active').order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user_investment = None
    
    if request.user.is_authenticated:
        user_investment = Investment.objects.filter(
            investor=request.user, 
            project=project,
            status='completed'
        ).first()
    
    context = {
        'project': project,
        'user_investment': user_investment,
        'days_remaining': (project.end_date - timezone.now()).days if project.end_date > timezone.now() else 0,
    }
    return render(request, 'projects/project_detail.html', context)

@login_required
def invest_in_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))
        
        if amount <= 0:
            messages.error(request, 'Investment amount must be greater than zero.')
            return redirect('project_detail', pk=pk)
        
        # Mock investment (no real payment processing)
        investment = Investment.objects.create(
            investor=request.user,
            project=project,
            amount=amount,
            status='completed',  # Normally would be 'pending' until payment confirmed
            payment_reference=f"MOCK-{uuid.uuid4().hex[:12].upper()}"
        )
        
        # Update project funding
        project.current_funding += amount
        if project.current_funding >= project.funding_goal:
            project.status = 'funded'
        project.save()
        
        messages.success(request, f'Successfully invested R{amount} in {project.title}!')
        return redirect('dashboard')
    
    return redirect('project_detail', pk=pk)

