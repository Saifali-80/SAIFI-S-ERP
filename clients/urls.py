from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.client_list, name='list'),
    path('add/', views.client_add, name='add'),
    path('<int:id>/', views.client_detail, name='detail'),
    path('<int:id>/edit/', views.client_edit, name='edit'),
    path('<int:id>/delete/', views.client_delete, name='delete'),
]