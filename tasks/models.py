from django.db import models
from django.contrib.auth.models import User
from categories.models import Category

# Create your models here.

class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
    class Priority(models.TextChoices):
        HIGH = "HIGH", 'High'
        MEDIUM = "MEDIUM", 'Medium'
        LOW = "LOW", 'Low'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')

    title = models.CharField(max_length=50)

    description = models.TextField(max_length=256, null=True, blank=True)

    priority = models.CharField(max_length=20, choices=Priority.choices , default=Priority.MEDIUM)

    status = models.CharField(max_length=20 , choices=Status.choices, default=Status.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    due_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['-created_at']