import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from clients.models import Client
from campaigns.models import Campaign
from tasks.models import Task
from invoicing.models import Invoice
from django.contrib.auth.models import User

user = User.objects.first()
if not user:
    user = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')

# Clients
c1 = Client.objects.create(name='Alpha Corp', email='alpha@test.com', phone='123', created_by=user, status='active')
c2 = Client.objects.create(name='Beta Ltd', email='beta@test.com', phone='456', created_by=user, status='active')
c3 = Client.objects.create(name='Gamma LLC', email='gamma@test.com', phone='789', created_by=user, status='lead')

# Campaigns
camp1 = Campaign.objects.create(name='SEO Q2', client=c1, campaign_type='seo', status='active', budget=5000, start_date='2025-04-01')
camp2 = Campaign.objects.create(name='Social Blast', client=c2, campaign_type='social', status='active', budget=3000, start_date='2025-04-10')
camp3 = Campaign.objects.create(name='Email Nurture', client=c3, campaign_type='email', status='planning', budget=1200, start_date='2025-05-01')

# Tasks
Task.objects.create(title='Keyword research', campaign=camp1, assigned_to=user, priority='high', due_date='2025-05-20', status='pending')
Task.objects.create(title='Ad copy', campaign=camp2, assigned_to=user, priority='medium', due_date='2025-05-18', status='in_progress')
Task.objects.create(title='Email template', campaign=camp3, assigned_to=user, priority='low', due_date='2025-05-25', status='pending')

# Invoices
Invoice.objects.create(invoice_number='INV-001', client=c1, amount=1500, tax=0, total_amount=1500, issue_date='2025-04-01', due_date='2025-05-01', status='paid')
Invoice.objects.create(invoice_number='INV-002', client=c2, amount=800, tax=80, total_amount=880, issue_date='2025-04-10', due_date='2025-05-10', status='sent')
print("Sample data added successfully!")