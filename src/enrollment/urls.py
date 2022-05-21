from django.urls import path
from enrollment.api_views import *
from rest_framework.authtoken import views

app_name = "course"
api_urlpatterns = [
    path('enroll', Enroll.as_view())
]

urlpatterns = [

]
