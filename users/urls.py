from django.urls import path

from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('<int:user_id>/carts', views.get_user_cart),
    path('<int:user_id>/carts/items', views.add_to_cart),
    path('<int:user_id>/carts/items/<int:cart_item_id>', views.update_or_delete_cart_item),
]
