# api_usuarios/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as token_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Configuración de Swagger/OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="API de Usuarios",
        default_version='v1',
        description="API para administrar usuarios",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@usuarios.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usuarios.urls')),
    path('api-token-auth/', token_views.obtain_auth_token, name='api_token_auth'),

    # URLs para la documentación con Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]