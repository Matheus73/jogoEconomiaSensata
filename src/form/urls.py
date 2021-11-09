from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('form/<int:id>/', views.render_form, name='form'),
    path('check/', views.check_form, name='check_form'),
    path('poll/', views.poll, name='poll'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('check_poll/', views.check_poll, name='check_poll'),
]
