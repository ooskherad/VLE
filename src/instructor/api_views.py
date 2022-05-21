from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin

from .serializers import InstructorSerializer
from helpers import SerializerContext


class CreateInstructorView(SerializerContext, APIView):
    serializer_class = InstructorSerializer

    def post(self, request):
        data = request.data
        user = request.user
        data.update(user_id=user.id)
        instructor = InstructorSerializer(data=data)
        if instructor.is_valid():
            instructor.save()

        return Response(data=instructor.data, status=status.HTTP_201_CREATED)
