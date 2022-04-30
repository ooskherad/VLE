from accounts.urls import api_urlpatterns as accounts_urls
from django.urls import path, include

api_urls = [
    path('accounts/', include(accounts_urls)),
]