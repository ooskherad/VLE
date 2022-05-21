from django.urls import path
from home.api_views import *

app_name = "home"
api_urlpatterns = [
    path('create_category', CreateCategory.as_view()),
    path('create_enumeration', CreateEnumerations.as_view()),
]

urlpatterns = [
    path('categories', GetCategories.as_view()),
]
