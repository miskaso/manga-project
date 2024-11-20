from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'popular', views.PopularView, basename='popular')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'review', views.ReviewView, basename='review')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
