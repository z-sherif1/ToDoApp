from django import forms
from .models import Task
from categories.models import Category


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'category',
            'priority',
            'status',
            'due_date',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = Category.objects.filter(user=user)