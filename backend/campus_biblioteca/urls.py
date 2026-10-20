from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(openapi.Info(title='Campus Biblioteca API', default_version='v1', description='Usuarios de la biblioteca universitaria. Login por email y autenticacion JWT.'), public=True, permission_classes=[AllowAny], authentication_classes=[])
urlpatterns = [path('admin/', admin.site.urls),path('api/v1/',include('users.urls')),path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='swagger'),path('redoc/',schema_view.with_ui('redoc',cache_timeout=0)),re_path(r'^swagger(?P<format>\.json|\.yaml)$',schema_view.without_ui(cache_timeout=0),name='schema-json')]
