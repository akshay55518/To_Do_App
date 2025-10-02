from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    
    # Admin Detail Section
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-approval/', views.admin_approval, name='admin_approval'),  
      
    # admin User Management
    path('admin-users/', views.user_details, name='user_list'),
    path('admin-users/edit/<int:pk>/', views.edit_user, name='edit_user'),
    path('admin-users/delete/<int:pk>/', views.delete_user, name='delete_user'),
    path('admin-users/<int:pk>/', views.admin_user_detail, name='admin_user_detail'),
    
    # admin Project Management
    path('admin-projects/', views.admin_project_list, name='admin_project_list'),
    path('admin-projects/add/', views.add_projects, name='add_projects'),
    path('admin-projects/edit/<int:pk>/', views.edit_project, name='edit_project'),
    path('admin-projects/delete/<int:pk>/', views.delete_project, name='delete_project'),
    
    # admin task management    
    path('admin-tasks/', views.admin_task_list, name='admin_task_list'),
    path('admin-tasks/add/', views.add_task, name='add_task'),
    path('admin-tasks/edit/<int:pk>/', views.edit_task, name='edit_task'),
    path('admin-tasks/delete/<int:pk>/', views.delete_task, name='delete_task'),

    
    # User Detail Section
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
]
