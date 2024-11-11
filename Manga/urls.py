from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

router = DefaultRouter()

router.register(r'show', views.SearchView, basename='showmanga')
router.register(r'authors', views.AuthorView, basename='authors')
router.register(r'tags', views.TagsView, basename='tags')
router.register(r'categories', views.CategoryView, basename='categories')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
