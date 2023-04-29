from django.urls import path

from . import views

urlpatterns = [
    path('brands', views.get_all_brands),
    path('laptops', views.get_all_laptops),
    path('laptops/<int:laptop_id>/configs', views.get_laptop_configs),
    path('products/<int:product_id>/images', views.get_product_images),
]
