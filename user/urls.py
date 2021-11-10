from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('check_register/', views.check_register, name='check_register'),
    path('check_signin/', views.check_signin, name='check_signin'),
    path('logout/', views.logout, name='logout'),
]
