from django.urls import path

from . import views

urlpatterns = [
    path('banners', views.get_all_banners),

]

