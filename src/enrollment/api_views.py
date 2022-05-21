from helpers import CreateAbstract as Create
from .serializers import EnrollmentSerializer
from rest_framework.permissions import IsAuthenticated


class CreateAbstract(Create):
    permission_classes = [IsAuthenticated, ]


class Enroll(CreateAbstract):
    serializer_class = EnrollmentSerializer

    def post(self, request):
        data = request.data
        user = request.user
        data.update(user=user.id)
        return self.create(data)
