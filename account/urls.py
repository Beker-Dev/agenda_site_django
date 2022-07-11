from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_account, name='view_account_index'),
    path('view/', views.view_account, name='view_account'),
    path('detail/<int:account_id>/', views.detail_account, name='detail_account'),
    path('remove/<int:account_id>/', views.remove_account, name='remove_account'),
    path('register/', views.register_account, name='register_account'),
    path('login/', views.login_account, name='login_account'),
    path('logout/', views.logout_account, name='logout_account'),
    path('search/', views.search_account, name='search_account'),
]
