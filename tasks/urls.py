from django.urls import path
from . import views
app_name='tasks'
urlpatterns = [
    path('', views.task_list, name='list'),
    path('add/', views.task_add, name='add'),
    path('<int:id>/edit/', views.task_edit, name='edit'),
    path('<int:id>/delete/', views.task_delete, name='delete'),
]