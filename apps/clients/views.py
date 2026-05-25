from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Client

@login_required
def client_list(request):
    clients = Client.objects.filter(created_by=request.user)
    return render(request, 'clients/list.html', {'clients': clients})

@login_required
def client_add(request):
    if request.method == 'POST':
        client = Client.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            company=request.POST.get('company', ''),
            address=request.POST.get('address', ''),
            status=request.POST.get('status', 'lead'),
            created_by=request.user
        )
        messages.success(request, 'Client added successfully!')
        return redirect('clients:detail', id=client.id)
    return render(request, 'clients/form.html')

@login_required
def client_detail(request, id):
    client = get_object_or_404(Client, id=id, created_by=request.user)
    return render(request, 'clients/detail.html', {'client': client})

@login_required
def client_edit(request, id):
    client = get_object_or_404(Client, id=id, created_by=request.user)
    if request.method == 'POST':
        client.name = request.POST['name']
        client.email = request.POST['email']
        client.phone = request.POST['phone']
        client.company = request.POST.get('company', '')
        client.address = request.POST.get('address', '')
        client.status = request.POST.get('status', 'lead')
        client.save()
        messages.success(request, 'Client updated successfully!')
        return redirect('clients:detail', id=client.id)
    return render(request, 'clients/form.html', {'client': client})

@login_required
def client_delete(request, id):
    client = get_object_or_404(Client, id=id, created_by=request.user)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client deleted successfully!')
        return redirect('clients:list')
    return render(request, 'clients/confirm_delete.html', {'client': client})