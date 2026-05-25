from django.urls import path
from . import views
app_name='invoicing'
urlpatterns = [
    path('', views.invoice_list, name='list'),
    path('add/', views.invoice_add, name='add'),
    path('<int:id>/', views.invoice_detail, name='detail'),
    path('<int:id>/edit/', views.invoice_edit, name='edit'),
    path('<int:id>/delete/', views.invoice_delete, name='delete'),
]