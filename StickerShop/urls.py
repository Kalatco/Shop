from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include
from products.views import ProductViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
