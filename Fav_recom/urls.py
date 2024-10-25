from django.urls import path, include
from .views import FavoriteView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'favorite', FavoriteView, basename='favorite')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]