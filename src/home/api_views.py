from helpers import CreateAbstract as Create
from home.serializers import CategorySerializer, EnumerationSerializer
from permissions import IsInstructor
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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
    permission_classes = [IsInstructor, ]


class CreateEnumerations(CreateAbstract):
    serializer_class = EnumerationSerializer
    permission_classes = [IsAdminUser, ]


class GetCategories(APIView):

    def get(self, request):
        """

        :param request:
        :return: categories with details
        """
        parents = Category.objects.filter(parent__isnull=True)
        data = {}
        for parent in parents:
            parent_categories = Category.objects.filter(parent_id=parent.id)
            parent_data = CategorySerializer(instance=parent).data
            parent_course_count = 0
            for category in parent_categories:
                categories_count = CourseCategories.objects.filter(category_id=category.id).aggregate(Count('course'))
                parent_course_count += categories_count['course__count']
                serializer = CategorySerializer(instance=category).data
                serializer.update(categories_count)
                parent_data.update(category=serializer)
            parent_data.update({'parent_course_count': 0})
            data.update(parent_data)
        return Response(data, status=status.HTTP_200_OK)
