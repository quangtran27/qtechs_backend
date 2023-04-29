from django.urls import path

from . import views

urlpatterns = [
    path("users", views.register, name='register'),
    path("auth/login", views.login, name="login"),
]
