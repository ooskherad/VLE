from django.urls import path
from course.api_views import *
from rest_framework.authtoken import views

app_name = "course"
api_urlpatterns = [
    path('create', CreateItemContentView.as_view()),
]

urlpatterns = [

]
