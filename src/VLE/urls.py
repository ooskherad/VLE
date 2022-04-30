from django.contrib import admin
from django.urls import path, include

from VLE.api_urls import api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/', include(api_urls)),
]
