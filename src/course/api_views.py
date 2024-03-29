import json
import random

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count, Aggregate
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http.response import HttpResponse
import mimetypes

from VLE.config import config
from helpers import CreateAbstract as Create
from home.services.file import FileService
from services.bucket_service import Bucket
from .serializers import *
from home.enumerations.group_file_enumerations import GroupFileEnums


class CreateAbstract(Create):
    permission_classes = [IsAuthenticated, ]


class CreateCoursesView(CreateAbstract):
    serializer_class = CourseSerializer

    def post(self, request):
        """
        ### owners parameter is optional now (it will need for add owner to a course)
        """
        data = request.data
        data = data.dict()
        data['categories'] = json.loads(data.get('categories'))
        user = request.user
        data.update(owners=[{'user': user.id}])
        if not data.get("statuses"):
            data["statuses"] = [
                {
                    "status_id": 11
                }
            ]
        if data.get('image') and data.get('image') != 'null':
            image = data.pop('image')
            file_service = FileService(file=image.file, file_name=image.name, user=request.user,
                                       group_file=GroupFileEnums.COURSE_FILES.value)
            file_name = file_service.upload_file()
            data.update(image=file_name.key)
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


# class CreateCourseSubSectionItemView(CreateAbstract):
#     serializer_class = CourseSubSectionItemSerializer
#
#     def post(self, request):
#         course_sub_section = get_object_or_404(CourseSubSections, id=request.data.get('course_sub_section'))
#         course_section = course_sub_section.course_section
#         course = course_section.course
#         self.check_object_permissions(request, course)
#         return self.create(request.data)


class CreateItemContentView(CreateAbstract):
    serializer_class = CourseSubSectionItemContentSerializer

    def post(self, request):
        data = request.data
        data = data.dict()
        course_sub_section = get_object_or_404(CourseSubSections,
                                               id=data.get('course_sub_section_item_id'))
        course_section = course_sub_section.course_section
        course = course_section.course
        self.check_object_permissions(request, course)
        file = request.FILES
        if file:
            data.pop('file')
            file_service = FileService(file=file.get('file').file, file_name=file.get('file').name, user=request.user,
                                       group_file=GroupFileEnums.COURSE_CONTENTS.value)
            file_instance = file_service.upload_and_save()
            data.update(file_id=file_instance.id)
        return self.create(data)


class GetCourseData(APIView):

    def get(self, request):
        """
        courseId as query parameter
        :param request:
        :return:
        """
        param = request.GET
        if param.get('courseId'):
            course_instance = Courses.objects.filter(id=int(param.get('courseId')))
            if course_instance:
                # instance = CourseSections.objects.filter(course_id=int(param.get('courseId')))
                # sections = CourseSectionSerializer(instance=instance, many=True)
                course = CourseSerializer(instance=course_instance, many=True)
                course.data[0]['image'] = config.ARVAN_URl + course.data[0]['image']
                return Response(course.data[0], status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetCourses(APIView):

    def get(self, request):
        """
        query_params: <int:limit = 6>, <str:order_by_field = -created_at> , <int:categories = None>, <int:id = None>
        :param q: query text for search in title
        :return: list of Courses
        """
        query_set = self.get_query_set(request.GET)
        return Response({'result': query_set}, status=status.HTTP_200_OK)

    def get_query_set(self, query_params):
        limit = int(query_params.get('limit')) if query_params.get('limit') else 6
        order_by_field = query_params.get('order_by_field') if query_params.get('order_by_field') else '-created_at'
        q = query_params.get('q')
        categories = query_params.get('categories')
        id = query_params.get('id')
        many = True
        if id:
            courses = get_object_or_404(Courses, id=id)
            many = False
        elif q:
            courses = Courses.objects.all().filter(title__contains=q).order_by(order_by_field)[:limit]
        elif categories:
            courses = Courses.objects.all().filter(categories__category_id=categories).order_by(order_by_field)[:limit]
        else:
            courses = Courses.objects.all().order_by(order_by_field)[:limit]

        if not courses:
            return []
        courses_serializer = CourseSerializer(instance=courses, many=many).data
        if isinstance(courses_serializer, list):
            for course in courses_serializer:
                sub_sections = course['sections'] if course['sections'] else []
                for section in sub_sections:
                    section.pop('sub_sections')
        return courses_serializer


class UserFeed(APIView):
    def get(self, request):
        try:
            params = request.GET
            limit = int(params.get('limit')) if params.get('limit') else 6
            courses = CourseSerializer(instance=self.get_query_set(limit), many=True, fields=['sections'])
            for course in courses.data:
                course["image"] = config.ARVAN_URl + course["image"]
            return Response(data=courses.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def get_query_set(self, limit):
        ids= Courses.objects.all().aggregate(arr=ArrayAgg('id'))
        limit = limit if limit < len(ids.get('arr')) else len(ids.get('arr'))
        # count = Courses.objects.aggregate(count=Count('id'))['count']
        # limit = limit if limit < count else count - 1
        # random_list = random.sample(range(1, 10), limit)
        random_list = random.sample(ids.get('arr'), k=limit)
        return Courses.objects.filter(id__in=random_list)


class GetCourseSubSections(APIView):
    def get(self, request):
        """
        <int:section (course_section_id)>
        :return: list of a CourseSections, 404 if not exist
        """
        param = request.GET
        if param.get('section'):
            instance = CourseSubSections.objects.filter(course_section_id=int(param.get('section')))
            if instance:
                sections = CourseSubSectionSerializer(instance=instance, many=True)
                return Response(sections.data, status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


# class GetCourseSubSectionItems(APIView):
#     def get(self, request):
#         """
#         <int:subsection (course_subsection_id)>
#         :return: list of a CourseSectionsItems, 404 if not exist
#         """
#         param = request.GET
#         if param.get('ssID'):
#             instance = CourseSubSectionItems.objects.filter(course_sub_section_id=int(param.get('ssID')))
#             if instance:
#                 sections = CourseSubSectionItemSerializer(instance=instance, many=True)
#                 return Response(sections.data, status.HTTP_200_OK)
#         return Response(status=status.HTTP_404_NOT_FOUND)


class GetContent(APIView):
    def get(self, request):
        """

        <int:item (course_item_id)>
        :return:list of content of an item,  404 if not exist
        """
        param = request.GET
        if param.get('subSection'):
            instance = CourseSubSectionItemContent.objects.filter(course_sub_section_item_id=int(param.get('subSection')))
            if instance:
                content = CourseSubSectionItemContentSerializer(instance=instance, many=True)
                for item in content.data:
                    item['file'] = config.ARVAN_URl + item.get('file')
                return Response(content.data, status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class DownloadContent(APIView):
    def get(self, request, file_name):
        filepath = Bucket().download_obj(file_name)
        mime_type, _ = mimetypes.guess_type(filepath)
        path = open(filepath, 'rb')
        response = HttpResponse(path.read(), content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % file_name
        return response
