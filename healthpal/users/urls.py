# healthpal/users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # رابط التسجيل
    # POST /api/v1/auth/register/
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    
    # رابط ملفي الشخصي
    # GET /api/v1/auth/me/
    # PATCH /api/v1/auth/me/
    path('me/', views.UserMeView.as_view(), name='user-me'),
]