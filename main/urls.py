from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.login_view, name='authorization/login'),
    path('registration/', views.registration_view, name='authorization/registration'),
    path('add_task/', views.add_task, name='create_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
]
