from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from .models import *
from django.contrib import messages

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin_user = authenticate(request, username=username, password=password)
        if admin_user is not None and admin_user.is_superuser:
            auth_login(request, admin_user)
            return redirect('admin_dashboard')
        try:
            normal_user = User.objects.get(username=username, password=password)
            if not normal_user.is_approved:
                messages.error(request, "Your account is not approved by admin yet.")
                return redirect('login')
            request.session['user_id'] = normal_user.id
            return redirect('user_dashboard')
        except User.DoesNotExist:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'auth/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username, email=email).exists():
            messages.error(request, "User with this username or email already exists")
            return redirect('register')
        user = User.objects.create(username=username, email=email, password=password)
        user.save()
        messages.success(request, "User registered successfully")
        return redirect('login')
    return render(request, 'auth/register.html')

def logout(request):
    request.session.flush()
    return redirect('login')

def admin_dashboard(request):
    total_projects = Project.objects.count()
    total_tasks = ToDo.objects.count()
    completed_tasks = ToDo.objects.filter(status='completed').count()
    pending_tasks = ToDo.objects.filter(status='pending').count()
    recent_tasks = ToDo.objects.order_by('-created_at')[:5]
    recent_projects = Project.objects.order_by('-created_at')[:5]
    context = {
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'recent_tasks': recent_tasks,
        'recent_projects': recent_projects
    }
    return render(request, 'admin/dashboard.html', context)

# admin approval
def admin_approval(request):
    users = User.objects.filter(is_approved=False)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = get_object_or_404(User, pk=user_id)
        if action == 'approve':
            user.is_approved = True
            user.save()
            messages.success(request, f"User {user.username} approved successfully")
        elif action == 'reject':
            user.delete()
            messages.success(request, f"User {user.username} rejected and deleted successfully")
        return redirect('admin_approval')
    return render(request, 'admin/approval.html', {'users': users})


# admin Users view
def user_details(request):
    user = User.objects.filter(is_approved=True)
    return render(request, 'admin/user/users.html', {'users': user})

def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exclude(pk=pk).exists():
            messages.error(request, "Username already taken")
            return redirect('edit_user', pk=pk)
        
        if User.objects.filter(email=email).exclude(pk=pk).exists():
            messages.error(request, "Email already taken")
            return redirect('edit_user', pk=pk)
        
        user.username = username
        user.email = email
        if password:
            user.password = password
        user.save()
        messages.success(request, "User updated successfully")
        return redirect('user_list')
    
    return render(request, 'admin/user/edit_user.html', {'user': user})

def admin_user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    tasks = ToDo.objects.filter(assigned_to=user)
    projects = Project.objects.filter(tasks__assigned_to=user).distinct()    
    return render(request, "admin/user/user_detail.html", {
        "user": user,
        "tasks": tasks,
        "projects": projects,
    })

def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully")
        return redirect('user_list')


    
# admin Projects
def admin_project_list(request):
    projects = Project.objects.all()
    return render(request, 'admin/project/projects.html', {'projects': projects})
    
def add_projects(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        project = Project.objects.create(name=name, description=description)
        project.save()
        messages.success(request, "Project added successfully")
        return redirect('admin_project_list')
    return render(request, 'admin/project/add_project.html')

def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        project.name = name
        project.description = description
        project.save()
        messages.success(request, "Project updated successfully")
        return redirect('admin_project_list')
    return render(request, 'admin/project/edit_project.html', {'project': project})

def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully")
        return redirect('admin_project_list')
    
# admin tasks
def admin_task_list(request):
    tasks = ToDo.objects.all().order_by('-created_at')
    return render(request, 'admin/task/tasks.html', {'tasks': tasks})

def add_task(request):
    projects = Project.objects.all()
    users = User.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        project_id = request.POST.get('project')
        assigned_to_id = request.POST.get('assigned_to')
        priority = request.POST.get('priority')
        status = request.POST.get('status')

        project = Project.objects.get(pk=project_id) if project_id else None
        assigned_to = User.objects.get(pk=assigned_to_id)

        task = ToDo.objects.create(
            title=title,
            description=description,
            project=project,
            assigned_to=assigned_to,
            priority=priority,
            status=status
        )
        task.save()
        messages.success(request, "Task added successfully")
        return redirect('admin_task_list')

    context = {
        'projects': projects,
        'users': users
    }
    return render(request, 'admin/task/add_tasks.html', context)

def edit_task(request, pk):
    task = get_object_or_404(ToDo, pk=pk)
    projects = Project.objects.all()
    users = User.objects.all()

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        project_id = request.POST.get('project')
        assigned_to_id = request.POST.get('assigned_to')
        task.priority = request.POST.get('priority')
        task.status = request.POST.get('status')

        task.project = Project.objects.get(pk=project_id) if project_id else None
        task.assigned_to = User.objects.get(pk=assigned_to_id)
        task.save()
        messages.success(request, "Task updated successfully")
        return redirect('admin_task_list')

    context = {
        'task': task,
        'projects': projects,
        'users': users
    }
    return render(request, 'admin/task/edit_tasks.html', context)

def delete_task(request, pk):
    task = get_object_or_404(ToDo, pk=pk)
    task.delete()
    messages.success(request, "Task deleted successfully")
    return redirect('admin_task_list')


def user_dashboard(request):
    return render(request, 'user/dashboard.html')