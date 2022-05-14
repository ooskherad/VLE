from django.urls import path
from course.api_views import *
from rest_framework.authtoken import views

app_name = "course"
api_urlpatterns = [
    path('create_course', CreateCoursesView.as_view()),
    path('create_section', CreateCourseSectionView.as_view()),
    path('create_subsection', CreateCourseSubSectionView.as_view()),
    path('create_item', CreateCourseSubSectionItemView.as_view()),
    path('create_item_content', CreateItemContentView.as_view()),
    path('ping', GetCourses.as_view())
]

urlpatterns = [

]
