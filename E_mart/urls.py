from E_mart.views import *
from django.urls import path

urlpatterns = [
    path('',HomeView.as_view(), name='home'),
    path('login/',LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('signup/',SignupView.as_view(), name='signup'),
    path('send-otp/',OtpSendView.as_view(), name='send_otp'),
    path('verify-otp/',VerifyOtpView.as_view(), name='verify_otp'),
]
