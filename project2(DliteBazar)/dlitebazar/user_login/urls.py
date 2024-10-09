from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('forgot-password', views.forgot_password, name='forgot_password'),
    
]