from django.urls import path
from instructor.api_views import *

app_name = "instructor"
api_urlpatterns = [
    path('create', CreateInstructorView.as_view()),
]

urlpatterns = [

]
