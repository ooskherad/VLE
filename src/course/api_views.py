from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin

from helpers import SerializerContext
from permissions import IsInstructor
from .serializers import *


class CreateAbstract(LoginRequiredMixin, APIView, SerializerContext):
    permission_classes = [IsInstructor, ]

    def create(self, data):
        try:
            instance = self.serializer_class(data=data)
        except Exception as error:
            return Response(data={'error': error.args[0] + ' not found in body'}, status=status.HTTP_400_BAD_REQUEST)

        if instance.is_valid():
            instance.save()
        else:
            return Response(data=instance.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=instance.data, status=status.HTTP_201_CREATED)


class CreateCoursesView(CreateAbstract):
    serializer_class = CourseSerializer

    def post(self, request):
        data = request.data
        data.update(user_id=request.user.id)
        return self.create(data)


class CreateCourseSectionView(CreateAbstract):
    serializer_class = CourseSectionSerializer

    def post(self, request):
        course = get_object_or_404(Courses, id=request.data.get('course_id'))
        self.check_object_permissions(request, course)
        return self.create(request.data)


class CreateCourseSubSectionView(CreateAbstract):
    serializer_class = CourseSubSectionSerializer

    def post(self, request):
        course = get_object_or_404(Courses, id=request.data.get('course_id'))
        course_section = get_object_or_404(CourseSections, id=request.data.get('course_section_id'))
        self.check_object_permissions(request, course)
        if course.id != course_section.course_id:
            return Response(data={'error': 'section does\'nt belongs to this course'}, status=status.HTTP_403_FORBIDDEN)
        return self.create(request.data)
