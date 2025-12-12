# healthpal/healthpal/urls.py

from django.contrib import admin
from django.urls import path, include

# --- (جديد) رح نستورد هدول ---
# (v2.0) الـ Views الجاهزة تاعت الـ Login (Token)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# (v2.0) الـ Views الجاهزة تاعت الـ Swagger (Documentation)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

     # --- (جديد) الروابط تاعت الـ API ---

    # 1. روابط الـ users (Register, Me)
    # رح يضيف /api/v1/auth/register/ و /api/v1/auth/me/
    path('api/v1/auth/', include('users.urls')),

    # 2. (v2.0) روابط الـ Login (الجاهزة من simplejwt)
    # (مطابق لتصميم v2.0 ملف 12، [cite: 562, 564])
    # POST /api/v1/auth/login/
    path('api/v1/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # POST /api/v1/auth/refresh/
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include('consultations.urls')),
    # 3. (v2.0) روابط الـ Swagger (التوثيق الآلي)
    # (مطابق لمتطلبات الدكتور [cite: 29])
    # GET /api/schema/
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # GET /api/schema/swagger-ui/
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # GET /api/schema/redoc/
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/sponsorship/', include('sponsorships.urls')),
    path('api/v1/inventory/', include('inventory.urls')),
    path('api/v1/education/', include('education.urls')),
    path('api/v1/support/', include('support.urls')),
    path('api/v1/ngo/', include('ngo.urls')),
]