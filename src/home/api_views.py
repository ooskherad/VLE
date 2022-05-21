from helpers import CreateAbstract as Create
from home.serializers import CategorySerializer, EnumerationSerializer
from permissions import IsInstructor
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category


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
        serializer = CategorySerializer(instance=parents, many=True)
        data = serializer.data
        for parent in data:
            category_serializer = CategorySerializer(instance=Category.objects.filter(parent_id=parent.get('id')),
                                                     many=True)
            parent.update(categoies=category_serializer.data)
        return Response(data, status=status.HTTP_200_OK)
