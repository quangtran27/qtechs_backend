from django.urls import path

from . import views

urlpatterns = [
    path('reviews/<int:review_id>', views.get_review),
]
