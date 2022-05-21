from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class SerializerContext:
    serializer_class = None

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)


class CreateAbstract(APIView, SerializerContext):

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