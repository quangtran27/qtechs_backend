from django.urls import path

from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('<int:user_id>', views.get_or_update_user_info),
    path('<int:user_id>/carts', views.get_user_cart),
    path('<int:user_id>/carts/items', views.add_to_cart),
    path('<int:user_id>/carts/items/<int:cart_item_id>', views.update_or_delete_cart_item),
    path('<int:user_id>/orders', views.get_orders_add_order),
    path('<int:user_id>/password', views.change_password),
]
