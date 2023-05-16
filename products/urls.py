from django.urls import path

from . import views

urlpatterns = [
    path('brands', views.get_all_brands),
    path('brands/<int:brand_id>', views.get_brand),
    path('categories', views.get_all_categories),
    path('categories/<int:category_id>', views.get_category),
    path('products', views.get_all_products),
    path('products/<int:product_id>', views.get_product),
    path('products/<int:product_id>/name', views.get_product_name),
]

