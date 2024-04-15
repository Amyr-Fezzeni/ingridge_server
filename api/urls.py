from django.urls import path
from . import views

urlpatterns = [
    path('send_email/', views.send_email_from_dashboard),
    path('request_otp/', views.request_otp),
    path('validate_otp/', views.verify_otp),
]
