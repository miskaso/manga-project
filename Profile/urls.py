from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import MyProfile, Register, LogoutView, ProfileView, RoleViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='roles')


urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
    path('myprof/', MyProfile.as_view(), name='profile'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('prof/', ProfileView.as_view(), name='viewprof'),

]