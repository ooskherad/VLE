from helpers import CreateAbstract as Create
from home.serializers import CategorySerializer, EnumerationSerializer
from home.models import Enumerations
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .enumerations import CourseLevelEnums
from .models import Category
from course.models import CourseCategories
from django.db.models import Count


class CreateAbstract(Create):
    def post(self, request):
        """

        :param request: <title:str>, <created_by=authenticated user>, <parent:id=None>
        :return:
        """
        try:
            data = request.data
            data.update(created_by=request.user.id)
            return self.create(data)
        except Exception as exception:
            return Response(data={'error': exception.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class CreateCategory(CreateAbstract):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, ]


class CreateEnumerations(CreateAbstract):
    serializer_class = EnumerationSerializer
    permission_classes = [IsAdminUser, ]


class GetCourseLevels(APIView):
    def get(self, request):
        levels = Enumerations.objects.filter(parent_id=CourseLevelEnums.parent.value)
        levels_serializer = EnumerationSerializer(instance=levels, many=True).data
        return Response(levels_serializer, status=status.HTTP_200_OK)


class GetCategories(APIView):

    def get(self, request):
        """

        :param request:
        :return: categories with details
        """
        parents = Category.objects.filter(parent__isnull=True)
        data = []
        for parent in parents:
            parent_categories = Category.objects.filter(parent_id=parent.id)
            parent_data = CategorySerializer(instance=parent).data
            parent_course_count = 0
            for category in parent_categories:
                categories_count = CourseCategories.objects.filter(category_id=category.id).aggregate(Count('course'))
                parent_course_count += categories_count['course__count']
                serializer = CategorySerializer(instance=category).data
                serializer.update(categories_count)
                parent_data.update(categories=serializer)
            parent_data.update({'parent_course_count': parent_course_count})
            data.append(parent_data)
            data.sort(key=lambda x: x.get('parent_course_count'), reverse=True)
        return Response(data, status=status.HTTP_200_OK)
