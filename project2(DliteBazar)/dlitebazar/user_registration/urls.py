from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_user, name='register_user'),
    path('email-verification/', views.email_verification, name='email_verification'),
]