from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'email', 'phone', 'category')
    list_display_links = ('name',)
    list_filter = ('category',)
    list_per_page = 10
    search_fields = ('id', 'name', 'surname', 'email', 'phone', 'category')
    list_editable = ()


admin.site.register(Contact, ContactAdmin)
