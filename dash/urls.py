from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # User CRUD
    path('all-users/', views.all_users_list, name='all_users_list'),
    path('user/add/', views.user_add, name='user_add'),
    path('user/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('user/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    
    # Client CRUD
    path('all-clients/', views.all_clients, name='all_clients'),
    path('client/add/', views.client_add, name='client_add'),
    path('client/<int:client_id>/edit/', views.client_edit, name='client_edit'),
    path('client/<int:client_id>/delete/', views.client_delete, name='client_delete'),
    
    # Campaign CRUD
    path('active-campaigns/', views.active_campaigns_list, name='active_campaigns_list'),
    path('campaign/add/', views.campaign_add, name='campaign_add'),
    path('campaign/<int:campaign_id>/edit/', views.campaign_edit, name='campaign_edit'),
    path('campaign/<int:campaign_id>/delete/', views.campaign_delete, name='campaign_delete'),
    
    # Task CRUD
    path('pending-tasks/', views.pending_tasks_list, name='pending_tasks_list'),
    path('in-progress-tasks/', views.in_progress_tasks_list, name='in_progress_tasks_list'),
    path('completed-tasks/', views.completed_tasks_list, name='completed_tasks_list'),
    path('task/add/', views.task_add, name='task_add'),
    path('task/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    
    # Invoice CRUD
    path('all-invoices/', views.all_invoices_list, name='all_invoices_list'),
    path('invoice/add/', views.invoice_add, name='invoice_add'),
    path('invoice/<int:invoice_id>/edit/', views.invoice_edit, name='invoice_edit'),
    path('invoice/<int:invoice_id>/delete/', views.invoice_delete, name='invoice_delete'),
    
    # Task Assignment
    path('task-assignment/', views.task_assignment, name='task_assignment'),
]