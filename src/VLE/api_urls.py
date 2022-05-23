from django.urls import path, include

from accounts.urls import api_urlpatterns as accounts_urls
from course.urls import api_urlpatterns as course_urls
from enrollment.urls import api_urlpatterns as enrollment_urls
from home.urls import api_urlpatterns as home_urls

api_urls = [
    path('home/', include(home_urls)),
    path('accounts/', include(accounts_urls)),
    path('course/', include(course_urls)),
    path('enrollment/', include(enrollment_urls)),
]