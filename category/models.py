from django.db import models
from django.utils import timezone
from django import forms


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    register_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('is_active', 'register_date')
