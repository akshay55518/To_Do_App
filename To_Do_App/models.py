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
        total = timedelta()
        for task in self.tasks.all():
            if task.time_spent:
                total += task.time_spent
        self.total_time_spent = total
        self.save()
        
    def formatted_total_time(self):
        """Return human-readable total time like '2h 43m 15s'."""
        total_seconds = int(self.total_time_spent.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"


class ToDo(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]

    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    assigned_to = models.ForeignKey("User", on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_time = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(default=timedelta)

    def __str__(self):
        return f"{self.title} ({self.priority})"

    def start_timer(self):
        if not self.start_time:  # only set if not already running
            self.start_time = timezone.now()
            self.status = "in_progress"
            self.save()

    def pause_timer(self):
        if self.start_time:
            now = timezone.now()
            elapsed = now - self.start_time
            self.time_spent = (self.time_spent or timedelta()) + elapsed
            self.start_time = None
            self.save()
            if self.project:
                self.project.update_total_time()  # Update total project time


    def stop_timer(self):
        self.pause_timer()
        self.status = "completed"
        self.completed = True
        self.save()
        if self.project:
            self.project.update_total_time()