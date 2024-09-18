from django.urls import path
from .views import *

urlpatterns = [
    path('register', register_user, name="register"),
    path('send-notification', send_notification, name="send-notification"),
]
