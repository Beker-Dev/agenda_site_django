from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_contact, name='view_contact_index'),
    path('view/', views.view_contact, name='view_contact'),
    path('register/', views.register_contact, name='register_contact'),
    path('detail/<int:contact_id>/', views.detail_contact, name='detail_contact'),
    path('remove/<int:contact_id>/', views.remove_contact, name='remove_contact'),
    path('search/', views.search_contact, name='search_contact'),
]
