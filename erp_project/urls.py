from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User
from clients.models import Client
from campaigns.models import Campaign
from tasks.models import Task
from invoicing.models import Invoice
import dash.views as dash_views

# ========== CUSTOM ADMIN SITE ==========
class CustomAdminSite(admin.AdminSite):
    site_header = "SAIFI'S ERP Admin Panel"
    site_title = "SAIFI'S ERP"
    index_title = "Dashboard"
    index_template = "admin/index.html"

    def index(self, request, extra_context=None):
        # REAL DATA COUNTS FROM DATABASE
        total_users = User.objects.count()
        total_clients = Client.objects.count()
        active_campaigns = Campaign.objects.filter(status='active').count()
        pending_tasks = Task.objects.filter(status='pending').count()
        total_revenue = Invoice.objects.filter(status='paid').aggregate(total=models.Sum('total_amount'))['total'] or 0

        # Recent items for recent actions sidebar
        recent_users = User.objects.all().order_by('-date_joined')[:5]
        recent_clients = Client.objects.all().order_by('-created_at')[:5]
        recent_campaigns = Campaign.objects.all().order_by('-created_at')[:5]
        recent_tasks = Task.objects.all().order_by('-created_at')[:5]
        recent_invoices = Invoice.objects.all().order_by('-created_at')[:5]

        context = {
            'total_users': total_users,
            'total_clients': total_clients,
            'active_campaigns': active_campaigns,
            'pending_tasks': pending_tasks,
            'total_revenue': total_revenue,
            'recent_users': recent_users,
            'recent_clients': recent_clients,
            'recent_campaigns': recent_campaigns,
            'recent_tasks': recent_tasks,
            'recent_invoices': recent_invoices,
            'user': request.user,
        }
        if extra_context:
            context.update(extra_context)
        return super().index(request, extra_context=context)

# Use custom admin site
admin.site = CustomAdminSite()
admin.autodiscover()

# ========== URL PATTERNS ==========
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', include('dash.urls')),
    path('clients/', include('clients.urls')),
    path('campaigns/', include('campaigns.urls')),
    path('tasks/', include('tasks.urls')),
    path('invoicing/', include('invoicing.urls')),
    
    # Filtered Views for Cards
    path('all-users/', dash_views.all_users_list, name='all_users_list'),
    path('all-clients/', dash_views.all_clients, name='all_clients'),
    path('pending-tasks/', dash_views.pending_tasks_list, name='pending_tasks_list'),
    path('in-progress-tasks/', dash_views.in_progress_tasks_list, name='in_progress_tasks_list'),
    path('completed-tasks/', dash_views.completed_tasks_list, name='completed_tasks_list'),
    path('active-campaigns/', dash_views.active_campaigns_list, name='active_campaigns_list'),
    
    # Task Assignment View
    path('task-assignment/', dash_views.task_assignment, name='task_assignment'),
]