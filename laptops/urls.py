from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_all_laptops),
    path('<int:laptop_id>', views.get_laptop),
    path('brands', views.get_all_laptop_brands),
    path('<int:laptop_id>/configs', views.get_laptop_configs),
]
