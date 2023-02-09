from django.urls import path, include
from . import views

urls = [
    path("", include("django.contrib.auth.urls")),
    path("signup/", views.signup, name="signup"),
]