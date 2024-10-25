from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'popular', views.PopularView, basename='popular')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('comments/', views.CommentsView.as_view(), name='comments'),
    path('review/', views.ReviewView.as_view(), name='review'),
    path('', include(router.urls)),
]
