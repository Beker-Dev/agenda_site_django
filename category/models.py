from django.db import models
from django.utils import timezone
from django import forms


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    register_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('register_date',)
