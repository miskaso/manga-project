from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import MyProfile, Register
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
    path('myprof/', MyProfile.as_view(), name='profile'),
    path('register/', Register.as_view(), name='register'),


]