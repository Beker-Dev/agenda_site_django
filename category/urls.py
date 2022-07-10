from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_category, name='view_category_index'),
    path('view/', views.view_category, name='view_category'),
    path('register/', views.register_category, name='register_category'),
    path('detail/<int:category_id>/', views.detail_category, name='detail_category'),
]
