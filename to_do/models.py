from django.db import models

# Create your models here.

class User(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=100)
    
    def __str__(self):
        return self.username

class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField()

    def __str__(self):
        return self.title
