from django.utils.text import slugify
from rest_framework import serializers
from django.db import transaction

from .models import *
from instructor.models import Instructor
from home.serializers import CategorySerializer, EnumerationSerializer


class CourseOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseOwners
        fields = ['instructor', ]


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategories
        fields = ['category']

    def to_representation(self, instance):
        return {'id': instance.category.id, 'title': instance.category.title}


class CourseSubSectionItemContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubSectionItemContent
        fields = ['id', 'course_sub_section_item', 'content', 'content_type_id']


class CourseSubSectionItemSerializer(serializers.ModelSerializer):
    sub_section_item_content = CourseSubSectionItemContentSerializer(many=True, read_only=True)

    class Meta:
        model = CourseSubSectionItems
        fields = ['id', 'course_sub_section', 'title', 'type', 'time_duration', 'price', 'created_at',
                  'sub_section_item_content']

    def validate_time_duration(self, attrs):
        if attrs <= 0:
            raise serializers.ValidationError('time duration must an positive integer number (in second) ')
        return attrs


class CourseSubSectionSerializer(serializers.ModelSerializer):
    sub_section_item = CourseSubSectionItemSerializer(many=True, read_only=True)

    class Meta:
        model = CourseSubSections
        fields = ['id', 'course_section', 'title', 'created_at', 'sub_section_item']


class CourseSectionSerializer(serializers.ModelSerializer):
    sub_sections = CourseSubSectionSerializer(many=True, read_only=True)

    class Meta:
        model = CourseSections
        fields = ['id', 'course', 'title', 'about_section', 'created_at', 'sub_sections']


class CourseSerializer(serializers.ModelSerializer):
    sections = CourseSectionSerializer(many=True, read_only=True)
    owners = CourseOwnerSerializer(many=True, write_only=True)
    categories = CourseCategorySerializer(many=True)
    course_level = serializers.StringRelatedField()

    class Meta:
        model = Courses
        fields = ['id', 'title', 'price', 'course_level', 'level', 'owners', 'categories', 'sections', ]

    def create(self, validated_data):
        owners = validated_data.pop('owners')
        categories = validated_data.pop('categories')
        with transaction.atomic():
            course = Courses.objects.create(**validated_data)
            for instructor in owners:
                CourseOwners.objects.create(course=course, instructor=instructor['instructor'])
            for category in categories:
                CourseCategories.objects.create(category=category['category'], course=course)

        return course
