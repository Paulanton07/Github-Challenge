from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/invest/', views.invest_in_project, name='invest_in_project'),
]
