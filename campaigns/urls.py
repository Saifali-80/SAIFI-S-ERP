from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('', views.campaign_list, name='list'),
    path('add/', views.campaign_add, name='add'),
    path('<int:id>/', views.campaign_detail, name='detail'),
    path('<int:id>/edit/', views.campaign_edit, name='edit'),
    path('<int:id>/delete/', views.campaign_delete, name='delete'),
]