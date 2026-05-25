from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Campaign
from clients.models import Client

@login_required
def campaign_list(request):
    campaigns = Campaign.objects.all()
    return render(request, 'campaigns/list.html', {'campaigns': campaigns})

@login_required
def campaign_add(request):
    if request.method == 'POST':
        client_id = request.POST.get('client')
        client = get_object_or_404(Client, id=client_id)
        
        campaign = Campaign.objects.create(
            name=request.POST['name'],
            client=client,
            campaign_type=request.POST['campaign_type'],
            status=request.POST.get('status', 'planning'),
            budget=request.POST.get('budget', 0),
            start_date=request.POST['start_date'],
            end_date=request.POST.get('end_date', None),
            description=request.POST.get('description', ''),
        )
        messages.success(request, 'Campaign added successfully!')
        return redirect('campaigns:detail', id=campaign.id)
    
    clients = Client.objects.all()
    return render(request, 'campaigns/form.html', {'clients': clients})

@login_required
def campaign_detail(request, id):
    campaign = get_object_or_404(Campaign, id=id)
    return render(request, 'campaigns/detail.html', {'campaign': campaign})

@login_required
def campaign_edit(request, id):
    campaign = get_object_or_404(Campaign, id=id)
    
    if request.method == 'POST':
        client_id = request.POST.get('client')
        campaign.client = get_object_or_404(Client, id=client_id)
        campaign.name = request.POST['name']
        campaign.campaign_type = request.POST['campaign_type']
        campaign.status = request.POST.get('status', 'planning')
        campaign.budget = request.POST.get('budget', 0)
        campaign.start_date = request.POST['start_date']
        campaign.end_date = request.POST.get('end_date', None)
        campaign.description = request.POST.get('description', '')
        campaign.save()
        
        messages.success(request, 'Campaign updated successfully!')
        return redirect('campaigns:detail', id=campaign.id)
    
    clients = Client.objects.all()
    return render(request, 'campaigns/form.html', {'campaign': campaign, 'clients': clients})

@login_required
def campaign_delete(request, id):
    campaign = get_object_or_404(Campaign, id=id)
    
    if request.method == 'POST':
        campaign.delete()
        messages.success(request, 'Campaign deleted successfully!')
        return redirect('campaigns:list')
    
    return render(request, 'campaigns/confirm_delete.html', {'campaign': campaign})