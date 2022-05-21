from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from VLE.api_urls import api_urls

schema_view = get_schema_view(
    openapi.Info(
        title="project API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    # swagger urls
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # app and api urls
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('home/', include('home.urls')),
    path('api/', include(api_urls)),
]
