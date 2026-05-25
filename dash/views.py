from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.contrib.auth.models import User
from clients.models import Client
from campaigns.models import Campaign
from tasks.models import Task
from invoicing.models import Invoice
from datetime import datetime, timedelta
import json


# ========== DASHBOARD VIEW ==========
@login_required
def dashboard(request):
    # Get filter parameters from request
    selected_year = request.GET.get('year', datetime.now().year)
    selected_month = request.GET.get('month', 'all')
    filter_type = request.GET.get('filter_type', 'last6')
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')
    
    try:
        selected_year = int(selected_year)
    except:
        selected_year = datetime.now().year
    
    # Stats Cards
    total_users = User.objects.count()
    total_clients = Client.objects.count()
    active_campaigns = Campaign.objects.filter(status='active').count()
    
    # Task Status Counts
    pending_tasks = Task.objects.filter(status='pending').count()
    in_progress_tasks = Task.objects.filter(status='in_progress').count()
    completed_tasks = Task.objects.filter(status='completed').count()
    
    # Task Assignment Stats
    users_with_tasks = User.objects.annotate(
        task_count=Count('tasks')
    ).filter(task_count__gt=0).count()
    
    total_assigned_tasks = Task.objects.count()
    total_revenue = Invoice.objects.filter(status='paid').aggregate(total=Sum('total_amount'))['total'] or 0

    # Monthly Revenue Chart
    revenue_labels = []
    revenue_data = []
    
    if filter_type == 'custom' and start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        current = start_date
        while current <= end_date:
            month_name = current.strftime('%b %Y')
            month_total = Invoice.objects.filter(
                status='paid',
                issue_date__year=current.year,
                issue_date__month=current.month
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            revenue_labels.append(month_name)
            revenue_data.append(float(month_total))
            
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1, day=1)
            else:
                current = current.replace(month=current.month + 1, day=1)
    
    elif filter_type == 'year' or (selected_month == 'all' and filter_type != 'last6'):
        year = selected_year
        for month in range(1, 13):
            month_name = datetime(year, month, 1).strftime('%b %Y')
            month_total = Invoice.objects.filter(
                status='paid',
                issue_date__year=year,
                issue_date__month=month
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            revenue_labels.append(month_name)
            revenue_data.append(float(month_total))
    
    elif selected_month != 'all':
        year = selected_year
        month = int(selected_month)
        for i in range(5, -1, -1):
            m = month - i
            y = year
            if m <= 0:
                m = 12 + m
                y = year - 1
            elif m > 12:
                m = m - 12
                y = year + 1
            month_name = datetime(y, m, 1).strftime('%b %Y')
            month_total = Invoice.objects.filter(
                status='paid',
                issue_date__year=y,
                issue_date__month=m
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            revenue_labels.append(month_name)
            revenue_data.append(float(month_total))
    else:
        today = datetime.now().date()
        for i in range(6):
            month_start = (today.replace(day=1) - timedelta(days=30*i)).replace(day=1)
            month_name = month_start.strftime('%b %Y')
            month_total = Invoice.objects.filter(
                status='paid',
                issue_date__year=month_start.year,
                issue_date__month=month_start.month
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            revenue_labels.insert(0, month_name)
            revenue_data.insert(0, float(month_total))

    # Campaign Performance Chart
    campaign_types = ['seo', 'social', 'email', 'ppc', 'content']
    type_labels = {
        'seo': 'SEO',
        'social': 'Social Media',
        'email': 'Email Marketing',
        'ppc': 'PPC/Google Ads',
        'content': 'Content Marketing'
    }
    
    campaign_counts = []
    campaign_labels = []
    for ct in campaign_types:
        count = Campaign.objects.filter(campaign_type=ct).count()
        campaign_counts.append(count)
        campaign_labels.append(type_labels[ct])

    # Recent Items
    recent_clients = Client.objects.all().order_by('-created_at')[:5]
    recent_campaigns = Campaign.objects.filter(status='active').order_by('-start_date')[:5]
    recent_invoices = Invoice.objects.all().order_by('-issue_date')[:5]
    recent_users = User.objects.all().order_by('-date_joined')[:5]
    recent_tasks = Task.objects.all().order_by('-created_at')[:5]

    years = list(range(2020, datetime.now().year + 2))
    months = [
        {'value': 'all', 'name': 'All Months'},
        {'value': '1', 'name': 'January'},
        {'value': '2', 'name': 'February'},
        {'value': '3', 'name': 'March'},
        {'value': '4', 'name': 'April'},
        {'value': '5', 'name': 'May'},
        {'value': '6', 'name': 'June'},
        {'value': '7', 'name': 'July'},
        {'value': '8', 'name': 'August'},
        {'value': '9', 'name': 'September'},
        {'value': '10', 'name': 'October'},
        {'value': '11', 'name': 'November'},
        {'value': '12', 'name': 'December'},
    ]

    context = {
        'total_users': total_users,
        'total_clients': total_clients,
        'active_campaigns': active_campaigns,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'total_revenue': total_revenue,
        'users_with_tasks': users_with_tasks,
        'total_assigned_tasks': total_assigned_tasks,
        'recent_clients': recent_clients,
        'recent_campaigns': recent_campaigns,
        'recent_invoices': recent_invoices,
        'recent_users': recent_users,
        'recent_tasks': recent_tasks,
        'revenue_labels': json.dumps(revenue_labels),
        'revenue_data': json.dumps(revenue_data),
        'campaign_labels': json.dumps(campaign_labels),
        'campaign_data': json.dumps(campaign_counts),
        'user': request.user,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'filter_type': filter_type,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'years': years,
        'months': months,
    }
    return render(request, 'dashboard.html', context)


# ========== USER CRUD VIEWS ==========
@login_required
def all_users_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard_filtered.html', {'items': users, 'title': 'All Users', 'type': 'user'})

@login_required
def user_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" already exists!')
        elif User.objects.filter(email=email).exists():
            messages.error(request, f'Email "{email}" already exists!')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', ''),
                is_staff=request.POST.get('is_staff') == 'on',
                is_active=request.POST.get('is_active') == 'on'
            )
            messages.success(request, f'User "{username}" created successfully!')
            return redirect('all_users_list')
    
    return render(request, 'crud_form.html', {'type': 'user', 'title': 'Add User'})

@login_required
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, f'Username "{username}" already exists!')
        elif User.objects.filter(email=email).exclude(id=user_id).exists():
            messages.error(request, f'Email "{email}" already exists!')
        else:
            user.username = username
            user.email = email
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.is_staff = request.POST.get('is_staff') == 'on'
            user.is_active = request.POST.get('is_active') == 'on'
            
            if request.POST.get('password'):
                user.set_password(request.POST.get('password'))
            
            user.save()
            messages.success(request, f'User "{user.username}" updated successfully!')
            return redirect('all_users_list')
    
    return render(request, 'crud_form.html', {'item': user, 'type': 'user', 'title': 'Edit User'})

@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = user.username
        if request.user.id == user_id:
            messages.error(request, 'You cannot delete your own account!')
        else:
            user.delete()
            messages.success(request, f'User "{username}" deleted successfully!')
        return redirect('all_users_list')
    
    return render(request, 'crud_confirm_delete.html', {'item': user, 'type': 'user', 'title': 'Delete User'})


# ========== CLIENT CRUD VIEWS ==========
@login_required
def all_clients(request):
    clients = Client.objects.all().order_by('-created_at')
    return render(request, 'dashboard_filtered.html', {'items': clients, 'title': 'All Clients', 'type': 'client'})

@login_required
def client_add(request):
    if request.method == 'POST':
        client = Client.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            company=request.POST.get('company', ''),
            address=request.POST.get('address', ''),
            status=request.POST.get('status', 'active')
        )
        messages.success(request, f'Client "{client.name}" created successfully!')
        return redirect('all_clients')
    
    return render(request, 'crud_form.html', {'type': 'client', 'title': 'Add Client'})

@login_required
def client_edit(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        client.name = request.POST.get('name')
        client.email = request.POST.get('email')
        client.phone = request.POST.get('phone')
        client.company = request.POST.get('company')
        client.address = request.POST.get('address')
        client.status = request.POST.get('status')
        client.save()
        messages.success(request, f'Client "{client.name}" updated successfully!')
        return redirect('all_clients')
    
    return render(request, 'crud_form.html', {'item': client, 'type': 'client', 'title': 'Edit Client'})

@login_required
def client_delete(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        name = client.name
        client.delete()
        messages.success(request, f'Client "{name}" deleted successfully!')
        return redirect('all_clients')
    
    return render(request, 'crud_confirm_delete.html', {'item': client, 'type': 'client', 'title': 'Delete Client'})


# ========== CAMPAIGN CRUD VIEWS ==========
@login_required
def active_campaigns_list(request):
    campaigns = Campaign.objects.filter(status='active').order_by('-start_date')
    return render(request, 'dashboard_filtered.html', {'items': campaigns, 'title': 'Active Campaigns', 'type': 'campaign'})

@login_required
def campaign_add(request):
    clients = Client.objects.all()
    
    if request.method == 'POST':
        client_id = request.POST.get('client')
        if not client_id:
            messages.error(request, 'Please select a client!')
            return render(request, 'crud_form.html', {
                'type': 'campaign', 
                'title': 'Add Campaign', 
                'clients': clients
            })
        
        campaign = Campaign.objects.create(
            name=request.POST.get('name'),
            client_id=client_id,
            campaign_type=request.POST.get('campaign_type'),
            budget=request.POST.get('budget', 0),
            status=request.POST.get('status', 'active'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date') or None,
            description=request.POST.get('description', '')
        )
        messages.success(request, f'Campaign "{campaign.name}" created successfully!')
        return redirect('active_campaigns_list')
    
    return render(request, 'crud_form.html', {
        'type': 'campaign', 
        'title': 'Add Campaign', 
        'clients': clients
    })

@login_required
def campaign_edit(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    clients = Client.objects.all()
    
    if request.method == 'POST':
        campaign.name = request.POST.get('name')
        campaign.client_id = request.POST.get('client')
        campaign.campaign_type = request.POST.get('campaign_type')
        campaign.budget = request.POST.get('budget')
        campaign.status = request.POST.get('status')
        campaign.start_date = request.POST.get('start_date')
        campaign.end_date = request.POST.get('end_date') or None
        campaign.description = request.POST.get('description')
        campaign.save()
        messages.success(request, f'Campaign "{campaign.name}" updated successfully!')
        return redirect('active_campaigns_list')
    
    return render(request, 'crud_form.html', {
        'item': campaign, 
        'type': 'campaign', 
        'title': 'Edit Campaign',
        'clients': clients
    })

@login_required
def campaign_delete(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    
    if request.method == 'POST':
        name = campaign.name
        campaign.delete()
        messages.success(request, f'Campaign "{name}" deleted successfully!')
        return redirect('active_campaigns_list')
    
    return render(request, 'crud_confirm_delete.html', {'item': campaign, 'type': 'campaign', 'title': 'Delete Campaign'})


# ========== TASK CRUD VIEWS ==========
@login_required
def pending_tasks_list(request):
    tasks = Task.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'dashboard_filtered.html', {'items': tasks, 'title': 'Pending Tasks', 'type': 'task'})

@login_required
def in_progress_tasks_list(request):
    tasks = Task.objects.filter(status='in_progress').order_by('-created_at')
    return render(request, 'dashboard_filtered.html', {'items': tasks, 'title': 'In Progress Tasks', 'type': 'task'})

@login_required
def completed_tasks_list(request):
    tasks = Task.objects.filter(status='completed').order_by('-created_at')
    return render(request, 'dashboard_filtered.html', {'items': tasks, 'title': 'Completed Tasks', 'type': 'task'})

@login_required
def task_add(request):
    campaigns = Campaign.objects.all()
    users = User.objects.all()
    
    if request.method == 'POST':
        task = Task.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            campaign_id=request.POST.get('campaign') or None,
            assigned_to_id=request.POST.get('assigned_to') or None,
            priority=request.POST.get('priority', 'medium'),
            status=request.POST.get('status', 'pending'),
            due_date=request.POST.get('due_date')
        )
        messages.success(request, f'Task "{task.title}" created successfully!')
        
        if task.status == 'pending':
            return redirect('pending_tasks_list')
        elif task.status == 'in_progress':
            return redirect('in_progress_tasks_list')
        else:
            return redirect('completed_tasks_list')
    
    return render(request, 'crud_form.html', {
        'type': 'task', 
        'title': 'Add Task', 
        'campaigns': campaigns, 
        'users': users
    })

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    campaigns = Campaign.objects.all()
    users = User.objects.all()
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.campaign_id = request.POST.get('campaign') or None
        task.assigned_to_id = request.POST.get('assigned_to') or None
        task.priority = request.POST.get('priority')
        task.status = request.POST.get('status')
        task.due_date = request.POST.get('due_date')
        task.save()
        messages.success(request, f'Task "{task.title}" updated successfully!')
        
        if task.status == 'pending':
            return redirect('pending_tasks_list')
        elif task.status == 'in_progress':
            return redirect('in_progress_tasks_list')
        else:
            return redirect('completed_tasks_list')
    
    return render(request, 'crud_form.html', {
        'item': task, 
        'type': 'task', 
        'title': 'Edit Task', 
        'campaigns': campaigns, 
        'users': users
    })

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        title = task.title
        status = task.status
        task.delete()
        messages.success(request, f'Task "{title}" deleted successfully!')
        
        if status == 'pending':
            return redirect('pending_tasks_list')
        elif status == 'in_progress':
            return redirect('in_progress_tasks_list')
        else:
            return redirect('completed_tasks_list')
    
    return render(request, 'crud_confirm_delete.html', {'item': task, 'type': 'task', 'title': 'Delete Task'})


# ========== INVOICE CRUD VIEWS (FIXED) ==========

@login_required
def all_invoices_list(request):
    invoices = Invoice.objects.all().order_by('-issue_date')
    return render(request, 'dashboard_filtered.html', {'items': invoices, 'title': 'All Invoices', 'type': 'invoice'})

@login_required
def invoice_add(request):
    clients = Client.objects.all()
    campaigns = Campaign.objects.all()
    
    if request.method == 'POST':
        invoice = Invoice.objects.create(
            invoice_number=request.POST.get('invoice_number'),
            client_id=request.POST.get('client'),
            campaign_id=request.POST.get('campaign') or None,
            total_amount=request.POST.get('total_amount'),
            tax=request.POST.get('tax', 0),
            status=request.POST.get('status', 'draft'),
            issue_date=request.POST.get('issue_date'),
            due_date=request.POST.get('due_date'),
            notes=request.POST.get('notes', ''),
            description=request.POST.get('description', '')  # Added description
        )
        messages.success(request, f'Invoice "{invoice.invoice_number}" created successfully!')
        return redirect('all_invoices_list')
    
    return render(request, 'crud_form.html', {
        'type': 'invoice', 
        'title': 'Add Invoice', 
        'clients': clients, 
        'campaigns': campaigns
    })

@login_required
def invoice_edit(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    clients = Client.objects.all()
    campaigns = Campaign.objects.all()
    
    if request.method == 'POST':
        invoice.invoice_number = request.POST.get('invoice_number')
        invoice.client_id = request.POST.get('client')
        invoice.campaign_id = request.POST.get('campaign') or None
        invoice.total_amount = request.POST.get('total_amount')
        invoice.tax = request.POST.get('tax', 0)
        invoice.status = request.POST.get('status')
        invoice.issue_date = request.POST.get('issue_date')
        invoice.due_date = request.POST.get('due_date')
        invoice.notes = request.POST.get('notes', '')
        invoice.description = request.POST.get('description', '')
        invoice.save()
        messages.success(request, f'Invoice "{invoice.invoice_number}" updated successfully!')
        return redirect('all_invoices_list')
    
    return render(request, 'crud_form.html', {
        'item': invoice, 
        'type': 'invoice', 
        'title': 'Edit Invoice', 
        'clients': clients, 
        'campaigns': campaigns
    })

@login_required
def invoice_delete(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == 'POST':
        number = invoice.invoice_number
        invoice.delete()
        messages.success(request, f'Invoice "{number}" deleted successfully!')
        return redirect('all_invoices_list')
    
    return render(request, 'crud_confirm_delete.html', {'item': invoice, 'type': 'invoice', 'title': 'Delete Invoice'})

# ========== TASK ASSIGNMENT VIEW ==========
@login_required
def task_assignment(request):
    users = User.objects.annotate(
        total_tasks=Count('tasks'),
        pending_count=Count('tasks', filter=Q(tasks__status='pending')),
        in_progress_count=Count('tasks', filter=Q(tasks__status='in_progress')),
        completed_count=Count('tasks', filter=Q(tasks__status='completed'))
    ).filter(total_tasks__gt=0).order_by('-total_tasks')
    
    total_assigned_tasks = Task.objects.count()
    
    selected_user_id = request.GET.get('user_id')
    user_tasks = None
    selected_user = None
    
    if selected_user_id:
        selected_user = get_object_or_404(User, id=selected_user_id)
        user_tasks = Task.objects.filter(assigned_to=selected_user).select_related('campaign')
    
    context = {
        'users': users,
        'selected_user': selected_user,
        'user_tasks': user_tasks,
        'total_assigned_tasks': total_assigned_tasks,
        'user': request.user,
    }
    return render(request, 'task_assignment.html', context)