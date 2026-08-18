from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ride/<int:pk>/', views.ride_detail, name='ride_detail'),
    path('ride/<int:pk>/book/', views.book_ride, name='book_ride'),
    path('create/', views.create_ride, name='create_ride'),
    path('login/', auth_views.LoginView.as_view(template_name='rides/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register')
]