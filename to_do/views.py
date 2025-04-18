from django.shortcuts import render, redirect, get_object_or_404
from .models import User, ToDo
from django.views.decorators.csrf import csrf_exempt

def login_register(request):
    if request.method == "POST":
        action = request.POST.get("action")
        username = request.POST.get("username")
        password = request.POST.get("password")
        if action == "register":
            if User.objects.filter(username=username).exists():
                error = "Username already taken"
                return render(request, "login.html", {"error": error})
            user = User.objects.create(username=username, password=password)
            user.save()
            return redirect(todo)
        elif action == "login":
            user = User.objects.filter(username=username, password=password)
            if user.exists():
                for i in user:
                    request.session["user_id"] = i.id
                    return redirect(todo)
            else:
                error = "Invalid username or password"
                return render(request, "login.html", {"error": error})
    return render(request, "login.html")

def todo(request):
    user_id = request.session.get("user_id")
    user = User.objects.get(id=user_id)
    sort = request.GET.get('filter')  
    if sort == "Done":
        todos = ToDo.objects.filter(user=user, completed=True).order_by("priority")
    elif sort == "Pending":
        todos = ToDo.objects.filter(user=user, completed=False).order_by("priority")
    else:
        todos = ToDo.objects.filter(user=user).order_by("priority")
    return render(request, "todo.html", {"data": [user], "todos": todos})

def add_todo(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("login")
        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority")
        user = User.objects.get(id=user_id)
        ToDo.objects.create(user=user, title=title, description=description, priority=priority)
        return redirect("todo")


def update_todo(request, id):
    todo = get_object_or_404(ToDo, id=id)
    if request.method == "POST":
        todo.title = request.POST.get("title")
        todo.description = request.POST.get("description")
        todo.priority = request.POST.get("priority")
        todo.save()
        return redirect("todo")
    return render(request, "update.html", {"todo": todo})


def delete_todo(request, id):
    if request.method == "POST":
        todo = get_object_or_404(ToDo, id=id)
        todo.delete()
        return redirect("todo")


def mark_done(request, id):
    if request.method == "POST":
        todo = get_object_or_404(ToDo, id=id)
        todo.completed = True
        todo.save()
        return redirect("todo")


def priority(request, id):
    if request.method == "POST":
        todo = get_object_or_404(ToDo, id=id)
        todo.priority = request.POST.get("priority")
        todo.save()
        return redirect("todo")


def logout(request):
    request.session.flush()
    return redirect("login_register")
