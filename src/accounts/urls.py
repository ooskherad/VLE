from django.urls import path
from accounts.api_views import *
from rest_framework.authtoken import views

app_name = "accounts"
api_urlpatterns = [
    path('register', UserRegistrationView.as_view()),
    path('verify_otp', UserRegistrationVerifyOtpView.as_view()),
    path('user/<int:id>', UserUpdateView.as_view()),
    path('auth', views.obtain_auth_token),
]

urlpatterns = [
    path('login', UserLogin.as_view()),
    path('profile/<int:id>', UserProfile.as_view()),
]
