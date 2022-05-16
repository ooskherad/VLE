from rest_framework import serializers
from .models import Instructor


class InstructorSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(write_only=True)

    class Meta:
        model = Instructor
        fields = ['title', 'about_you', 'user', 'created_at']
