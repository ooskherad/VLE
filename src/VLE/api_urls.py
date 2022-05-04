from django.urls import path, include

from accounts.urls import api_urlpatterns as accounts_urls
from course.urls import api_urlpatterns as course_urls


api_urls = [
    path('accounts/', include(accounts_urls)),
    path('course/', include(course_urls)),
]