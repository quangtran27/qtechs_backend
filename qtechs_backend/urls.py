from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

from users.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login', login, name='login'),
    path('api/', include('products.urls')),
    path('api/promotions/', include('promotions.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/users/', include('users.urls')),
    path('api/carts/', include('carts.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)