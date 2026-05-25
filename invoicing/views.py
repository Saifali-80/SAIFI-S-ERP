from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Invoice
from clients.models import Client

@login_required
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoicing/list.html', {'invoices': invoices})

@login_required
def invoice_add(request):
    if request.method == 'POST':
        client = get_object_or_404(Client, id=request.POST['client'])
        amount = float(request.POST['amount'])
        tax = float(request.POST.get('tax', 0))
        Invoice.objects.create(
            invoice_number=request.POST['invoice_number'],
            client=client,
            amount=amount,
            tax=tax,
            total_amount=amount+tax,
            issue_date=request.POST['issue_date'],
            due_date=request.POST['due_date'],
            status=request.POST.get('status','draft'),
            notes=request.POST.get('notes','')
        )
        messages.success(request, 'Invoice added.')
        return redirect('invoicing:list')
    clients = Client.objects.all()
    return render(request, 'invoicing/form.html', {'clients': clients})

@login_required
def invoice_detail(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    return render(request, 'invoicing/detail.html', {'invoice': invoice})

@login_required
def invoice_edit(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    if request.method == 'POST':
        invoice.client_id = request.POST['client']
        invoice.amount = request.POST['amount']
        invoice.tax = request.POST.get('tax',0)
        invoice.total_amount = float(invoice.amount)+float(invoice.tax)
        invoice.issue_date = request.POST['issue_date']
        invoice.due_date = request.POST['due_date']
        invoice.status = request.POST.get('status','draft')
        invoice.notes = request.POST.get('notes','')
        invoice.save()
        messages.success(request, 'Invoice updated.')
        return redirect('invoicing:list')
    clients = Client.objects.all()
    return render(request, 'invoicing/form.html', {'invoice': invoice, 'clients': clients})

@login_required
def invoice_delete(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, 'Invoice deleted.')
        return redirect('invoicing:list')
    return render(request, 'invoicing/confirm_delete.html', {'invoice': invoice})