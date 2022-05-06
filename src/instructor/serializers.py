from rest_framework import serializers
from .models import Instructor


class InstructorSerializer(serializers.Serializer):
    title = serializers.CharField()
    about_you = serializers.CharField()
    user_id = serializers.IntegerField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return Instructor.objects.create(**validated_data)
