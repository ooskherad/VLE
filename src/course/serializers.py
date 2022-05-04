from django.utils.text import slugify
from rest_framework import serializers
from django.db import transaction

from .models import Courses, CourseCategories, CourseOwners, CourseSections
from instructor.models import Instructor


class CourseSectionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    about_section = serializers.CharField()
    course_id = serializers.IntegerField()

    def create(self, validated_data):
        return CourseSections.objects.create(
            course_id=validated_data['course_id'],
            title=validated_data['title'],
            about_section=validated_data['about_section'],
        )

    def update(self, instance, validated_data):
        pass


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    price = serializers.FloatField(default=0)
    level = serializers.IntegerField()
    categories = serializers.ListField()

    def create(self, validated_data):
        slug = validated_data.get('title')
        validated_data.update(slug=slugify(slug))
        with transaction.atomic():
            course = Courses.objects.create(**validated_data)
            instructor = Instructor.objects.get(serializers.CurrentUserDefault)
            CourseOwners.objects.create(instructor=instructor)
            for category in validated_data.get('categories'):
                CourseCategories.objects.create(course=course, category=category)
        return course

    def update(self, instance, validated_data):
        pass
