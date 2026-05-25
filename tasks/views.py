from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from campaigns.models import Campaign

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/list.html', {'tasks': tasks})

@login_required
def task_add(request):
    if request.method == 'POST':
        campaign = get_object_or_404(Campaign, id=request.POST['campaign'])
        Task.objects.create(
            title=request.POST['title'],
            description=request.POST.get('description',''),
            campaign=campaign,
            assigned_to=request.user,
            priority=request.POST.get('priority','medium'),
            status=request.POST.get('status','pending'),
            due_date=request.POST['due_date']
        )
        messages.success(request, 'Task added.')
        return redirect('tasks:list')
    campaigns = Campaign.objects.all()
    return render(request, 'tasks/form.html', {'campaigns': campaigns})

@login_required
def task_edit(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST.get('description','')
        task.campaign_id = request.POST['campaign']
        task.priority = request.POST.get('priority','medium')
        task.status = request.POST.get('status','pending')
        task.due_date = request.POST['due_date']
        task.save()
        messages.success(request, 'Task updated.')
        return redirect('tasks:list')
    campaigns = Campaign.objects.all()
    return render(request, 'tasks/form.html', {'task': task, 'campaigns': campaigns})

@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
        return redirect('tasks:list')
    return render(request, 'tasks/confirm_delete.html', {'task': task})