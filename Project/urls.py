"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

GOOGLE_CLIENT_ID = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
GOOGLE_CLIENT_SECRET = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['secret']

REDIRECT_URI = "https://a993-31-192-250-125.ngrok-free.app/api/auth/google/callback/"

class GoogleLoginView(APIView):
    def get(self, request):
        auth_url = (
            f"https://accounts.google.com/o/oauth2/auth?"
            f"client_id={GOOGLE_CLIENT_ID}&"
            f"redirect_uri={REDIRECT_URI}&"
            f"response_type=code&"
            f"scope=openid email profile&"
            f"prompt=consent"
        )
        return redirect(auth_url)

class GoogleAuthCallbackView(APIView):
    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Получение access_token от Google
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()

        access_token = token_json.get("access_token")
        if not access_token:
            return Response({"error": "Failed to obtain access token"}, status=status.HTTP_400_BAD_REQUEST)

        # Получение информации о пользователе с помощью access_token
        userinfo_endpoint = "https://www.googleapis.com/oauth2/v3/userinfo"
        userinfo_response = requests.get(
            userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info = userinfo_response.json()

        if userinfo_response.status_code != 200:
            return Response({"error": "Failed to fetch user info from Google"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "email": user_info.get("email"),
            "name": user_info.get("name"),
        })

schema_view = get_schema_view(
    openapi.Info(
        title="Документация API",
        default_version='v1',
        description="Документация к проекту Манга",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('Profile.urls')),
    path('manga/', include('Manga.urls')),
    path('fiches/', include('Fiches.urls')),
    path('fav_recom/', include('Fav_recom.urls')),
    path('reviews/', include('Reviews.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/social/', include('allauth.urls')),
    path('auth/', include('dj_rest_auth.urls')),  # JWT-эндпоинты
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  # Регистрация
    path('auth/social/', include('allauth.socialaccount.urls')),
    path('api/auth/google/login/', GoogleLoginView.as_view(), name='google_login'),
    path('api/auth/google/callback/', GoogleAuthCallbackView.as_view(), name='google_callback'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
