from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin

from helpers import SerializerContext
from home.services.file import FileService
from permissions import IsInstructor
from .serializers import *


class CreateAbstract(APIView, SerializerContext):
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
        """
        ### owners parameter is optional now (it will need for add owner to a course)
        """
        data = request.data
        instructor = Instructor.objects.get(user=request.user)
        data.update(owners=[{'instructor': instructor.id}])
        return self.create(data)


class CreateCourseSectionView(CreateAbstract):
    serializer_class = CourseSectionSerializer

    def post(self, request):
        course = get_object_or_404(Courses, id=request.data.get('course'))
        self.check_object_permissions(request, course)
        return self.create(request.data)


class CreateCourseSubSectionView(CreateAbstract):
    serializer_class = CourseSubSectionSerializer

    def post(self, request):
        course_section = get_object_or_404(CourseSections, id=request.data.get('course_section'))
        course = course_section.course
        self.check_object_permissions(request, course)
        return self.create(request.data)


class CreateCourseSubSectionItemView(CreateAbstract):
    serializer_class = CourseSubSectionItemSerializer

    def post(self, request):
        course_sub_section = get_object_or_404(CourseSubSections, id=request.data.get('course_sub_section'))
        course_section = course_sub_section.course_section
        course = course_section.course
        self.check_object_permissions(request, course)
        return self.create(request.data)


class CreateItemContentView(CreateAbstract):
    serializer_class = CourseSubSectionItemContentSerializer

    def post(self, request):
        course_sub_section_item = get_object_or_404(CourseSubSectionItems, id=request.data.get('course_sub_section_item'))
        course_sub_section = course_sub_section_item.course_sub_section
        course_section = course_sub_section.course_section
        course = course_section.course
        self.check_object_permissions(request, course)
        file = request.FILES
        if file:
            file_service = FileService(file=file.get('file').file, file_name=file.get('file').name, user=request.user)
            file_instance = file_service.upload_and_save()
            request.data.update(file_id=file_instance.id)
        return self.create(request.data)


class GetCourses(APIView):

    def get(self, request):
        """
        query_params: <int:limit = 6>, <str:order_by_field = -created_at>
        :param q: query text for search in title
        :return: list of Courses
        """
        query_set = self.get_query_set(request.GET)
        return Response({'result': query_set}, status=status.HTTP_200_OK)

    def get_query_set(self, query_params):
        limit = int(query_params.get('limit')) if query_params.get('limit') else 6
        order_by_field = query_params.get('order_by_field') if query_params.get('order_by_field') else '-created_at'
        q = query_params.get('q')
        if q:
            courses = Courses.objects.all().filter(title__contains=q).order_by(order_by_field)[:limit]
        else:
            courses = Courses.objects.all().order_by(order_by_field)[:limit]

        if not courses:
            return []
        data = []
        for course in courses:
            course_serializer = CourseSerializer(instance=course).data
            data.append(course_serializer)

        return data
