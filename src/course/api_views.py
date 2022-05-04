from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin

from helpers import SerializerContext
from permissions import IsInstructor
from .serializers import *


class CreateCoursesView(APIView, SerializerContext):
    permission_classes = [IsInstructor, ]
    serializer_class = CourseSerializer

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        return super().setup(request, *args, **kwargs)

    def post(self, request):
        data = request.data
        try:
            course = self.serializer_class(
                data={
                    'title': data['title'],
                    'level': data['level'],
                    'price': data['price'],
                    'categories': data['categories'],
                }
            )
        except Exception as error:
            return Response(data={'error': error.args[0] + ' not found in body'}, status=status.HTTP_400_BAD_REQUEST)

        if course.is_valid():
            course.save()
        else:
            return Response(data=course.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=course.data, status=status.HTTP_201_CREATED)


class CreateCourseSectionView(APIView, SerializerContext):
    permission_classes = [IsInstructor, ]
    serializer_class = CourseSectionSerializer

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        self.course = get_object_or_404(Courses, id=request.data.get('course_id'))
        return super().setup(request, *args, **kwargs)

    def post(self, request):
        data = request.data
        self.check_object_permissions(request, self.course)
        try:
            course_section = self.serializer_class(
                data={
                    'course_id': self.course.id,
                    'title': data['title'],
                    'about_section': data['about_section'],
                }
            )
        except Exception as error:
            return Response(data={'error': error.args[0] + ' not found in body'}, status=status.HTTP_400_BAD_REQUEST)
        if course_section.is_valid():
            course_section.save()
        else:
            return Response(data=course_section.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=course_section.data, status=status.HTTP_201_CREATED)


class CreateCourseSubSectionView(APIView, SerializerContext):
    permission_classes = [IsInstructor, ]
    serializer_class = CourseSubSectionSerializer

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        self.course = get_object_or_404(Courses, id=request.data.get('course_id'))
        self.course_section = get_object_or_404(CourseSections, id=request.data.get('course_section_id'))
        return super().setup(request, *args, **kwargs)

    def post(self, request):
        data = request.data
        if self.course.id != self.course_section.course_id:
            return Response(data={'error': 'section does\'nt belongs to this course'}, status=status.HTTP_403_FORBIDDEN)
        self.check_object_permissions(request, self.course)
        try:
            course_section = self.serializer_class(
                data={
                    'course_section_id': self.course.id,
                    'title': data['title'],
                }
            )
        except Exception as error:
            return Response(data={'error': error.args[0] + ' not found in body'}, status=status.HTTP_400_BAD_REQUEST)
        if course_section.is_valid():
            course_section.save()
        else:
            return Response(data=course_section.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=course_section.data, status=status.HTTP_201_CREATED)
