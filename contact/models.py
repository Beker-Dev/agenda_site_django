from django.db import models
from django.utils import timezone
from django import forms
from category.models import Category


class Contact(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    email = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    register_date = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%m/%d/')

    def __str__(self):
        return self.name


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('register_date',)
