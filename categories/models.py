from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='categories')
    name = models.CharField (max_length=50)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user','name'],
                name= 'unique_category_name_per_user'
            )
        ]
        ordering = ['name']