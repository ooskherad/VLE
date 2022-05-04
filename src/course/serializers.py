from django.utils.text import slugify
from rest_framework import serializers
from django.db import transaction

from .models import Courses, CourseCategories, CourseOwners, CourseSections, CourseSubSections
from instructor.models import Instructor


class CourseSectionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    about_section = serializers.CharField()
    course_id = serializers.IntegerField(write_only=True)

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
    level_id = serializers.IntegerField()
    categories = serializers.ListField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        slug = validated_data.get('title')
        validated_data.update(slug=slugify(slug))
        categories = validated_data.pop('categories')
        user_id = validated_data.pop('user_id')
        with transaction.atomic():
            # todo: status
            course = Courses.objects.create(**validated_data)
            instructor = Instructor.objects.get(user_id=user_id)
            CourseOwners.objects.create(instructor=instructor, course=course)
            for category in categories:
                CourseCategories.objects.create(course=course, category_id=category)
        return course

    def update(self, instance, validated_data):
        pass


class CourseSubSectionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    course_section_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        return CourseSubSections.objects.create(
            course_section_id=validated_data['course_section_id'],
            title=validated_data['title'],
        )

    def update(self, instance, validated_data):
        pass
