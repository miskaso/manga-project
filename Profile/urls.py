from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import (MyProfile, Register, LogoutView, ProfileView,
                    AssignGroupView, VerifySMSView, pay_account)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
    path('myprof/', MyProfile.as_view(), name='profile'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('prof/', ProfileView.as_view(), name='viewprof'),
    path('assign-role/', AssignGroupView.as_view(), name='assign_role'),
    path('verify-sms/', VerifySMSView.as_view(), name='verify-sms'),
    path('pay/', pay_account, name='pay'),

]
