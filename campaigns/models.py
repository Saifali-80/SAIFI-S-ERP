from django.db import models
from clients.models import Client

class Campaign(models.Model):
    TYPE_CHOICES = [
        ('seo', 'SEO'),
        ('social', 'Social Media'),
        ('email', 'Email Marketing'),
        ('ppc', 'Google Ads/PPC'),
        ('content', 'Content Marketing'),
    ]
    
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]
    
    name = models.CharField(max_length=200)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='campaigns')
    campaign_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.client.name}"
    
    class Meta:
        ordering = ['-created_at']