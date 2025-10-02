from django.contrib import admin
from .models import User, Project, ToDo

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    search_fields = ("username", "email")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "total_time_spent")
    search_fields = ("name",)
    list_filter = ("created_at",)


@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ("title", "assigned_to", "project", "priority", "status", "created_at")
    search_fields = ("title", "assigned_to__username", "project__name")
    list_filter = ("priority", "status", "created_at")
