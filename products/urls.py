from django.urls import path

from . import views

urlpatterns = [
    path('brands', views.get_all_brands),
    path('products/<int:product_id>/images', views.get_product_images),
]
