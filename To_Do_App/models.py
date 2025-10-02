from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)  # Admin approval

    def __str__(self):
        return self.username

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Timer field for project total time
    total_time_spent = models.DurationField(default=timedelta, blank=True)

    def __str__(self):
        return self.name

    def update_total_time(self):
        """Recalculate total time spent from all tasks in this project."""
        total = timedelta()
        for task in self.tasks.all():
            if task.time_spent:
                total += task.time_spent
        self.total_time_spent = total
        self.save()


class ToDo(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Timer fields for the task
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(null=True, blank=True)  # total time spent on task

    def __str__(self):
        return f"{self.title} ({self.priority})"

    # ---------------- Timer methods ----------------
    def start_timer(self):
        self.start_time = timezone.now()
        self.save()

    def stop_timer(self):
        if self.start_time:
            self.end_time = timezone.now()
            self.time_spent = self.end_time - self.start_time
            self.save()
            # Update project total time automatically
            if self.project:
                self.project.update_total_time()