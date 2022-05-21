from django.core.management.base import BaseCommand
from django.db import connection

from accounts.serializers import UserSerializer, User
from instructor.serializers import InstructorSerializer
from course.serializers import CourseSerializer, CourseSectionSerializer, CourseSubSectionSerializer, \
    CourseSubSectionItemSerializer, CourseSubSectionItemContentSerializer
from home.serializers import CategorySerializer, EnumerationSerializer
from home.models import Enumerations, Category, FileGroup
from home.models import Files
import home.enumerations as enumerations


class Command(BaseCommand):
    help = 'create test data'

    def handle(self, *args, **options):
        user_data = [{
            'mobile': '09372978889',
            'password': 1234,
        }]
        users = UserSerializer(data=user_data, many=True)
        users.is_valid()
        users.save()
        if users.errors:
            print(users.errors)
            return
        print('user_created')
        user = User.objects.get(mobile='09372978889')

        instructor_data = {
            'user': user.id,
            'title': 'Untitled',
            'about_yot': 'I Love Python',

        }
        instructor = InstructorSerializer(data=instructor_data)
        instructor.is_valid()
        if instructor.errors:
            print(instructor.errors)
            return
        instructor.save()
        print('instructor_created')

        category_data = [
            {
                'title': 'programming',
                'created_by': user.id,
            },
            {
                'title': 'physic',
                'created_by': user.id,
            }
        ]

        category = CategorySerializer(data=category_data, many=True)
        category.is_valid()
        if category.errors:
            print(category.errors)
            return
        category.save()
        print('category_created')

        course_data = [
            {
                "title": "آموزش پایتون",
                "price": 0,
                "level_id": Enumerations.objects.get(title='hard').id,
                "categories": [
                    {
                        "category": Category.objects.get(title='programming').id
                    }
                ],
                "owners": [
                    {
                        "instructor": 1
                    }
                ],
                "statuses": [
                    {
                        "status_id": Enumerations.objects.get(title='active').id
                    }
                ]
            },
            {
                "title": "آموزش فیزیک",
                "price": 12000,
                "level_id": Enumerations.objects.get(title='hard').id,
                "categories": [
                    {
                        "category": Category.objects.get(title='physic').id
                    }
                ],
                "owners": [
                    {
                        "instructor": 1
                    }
                ],
                "statuses": [
                    {
                        "status_id": Enumerations.objects.get(title='active').id
                    }
                ]
            }
        ]

        courses = CourseSerializer(data=course_data, many=True)
        courses.is_valid()
        if courses.errors:
            print(courses.errors)
            return
        courses.save()
        section_data = [
            {
                'course': 1,
                'title': 'فضل اول',
                'about_section': 'در این فصل به بررسی آن ها می پردازیم'
            }, {
                'course': 1,
                'title': 'فضل دوم',
                'about_section': 'در این فصل به بررسی این ها می پردازیم'
            }, {
                'course': 1,
                'title': 'فضل سوم',
                'about_section': 'در این فصل به بررسی اون ها می پردازیم'
            },
        ]
        sections = CourseSectionSerializer(data=section_data, many=True)
        sections.is_valid()
        if sections.errors:
            print(sections.errors)
            return
        sections.save()

        sub_data = [
            {
                'course_section': 1,
                'title': 'مقدمه'
            },
            {
                'course_section': 1,
                'title': 'شروع کار'
            },
            {
                'course_section': 1,
                'title': 'فایل های درس'
            }
        ]
        sub = CourseSubSectionSerializer(data=sub_data, many=True)
        sub.is_valid()
        if sub.errors:
            print(sub.errors)
            return
        sub.save()

        item_data = [
            {
                'course_sub_section': 1,
                'title': 'آشنایی با فصل',
                'type': Enumerations.objects.get(title='video').id,
                'time_duration': 180,
                'price': 0,
            }, {
                'course_sub_section': 2,
                'title': 'بخش ۱',
                'type': Enumerations.objects.get(title='video').id,
                'time_duration': 180,
                'price': 0,
            }, {
                'course_sub_section': 2,
                'title': 'بخش ۲',
                'type': Enumerations.objects.get(title='video').id,
                'time_duration': 180,
                'price': 0,
            }, {
                'course_sub_section': 2,
                'title': 'آزمون فصل ۱ و ۲',
                'type': Enumerations.objects.get(title='video').id,
                'time_duration': 180,
                'price': 0,
            }, {
                'course_sub_section': 3,
                'title': 'جزوه فصل ۱ و۲',
                'type': Enumerations.objects.get(title='video').id,
                'time_duration': 180,
                'price': 0,
            }
        ]
        items = CourseSubSectionItemSerializer(data=item_data, many=True)
        items.is_valid()
        if items.errors:
            print(items.errors)
            return
        items.save()

        group = FileGroup(name='course_content', path='/course/content/')
        group.save()
        video_file = Files(
            type='video',
            format='.mp4',
            title='6973ac72bef1e5a95695fc6f5d62197d44933466-360p',
            size=3338,
            created_by=user,
            group=group,
        )
        video_file.save()
        image_file = Files(
            type='image',
            format='.jpg',
            title='e9aebd8d378574715a9dda9aa746c966',
            size=3338,
            created_by=user,
            group_id=1,
        )
        image_file.save()
        content_data = [
            {
                'course_sub_section_item': 1,
                'content': None,
                'content_type': Enumerations.objects.get(title='video').id,
                'file': video_file.id
            }, {
                'course_sub_section_item': 2,
                'content': 'توضیحاتی در مورد درس, توضیحاتی در مورد درس, توضیحاتی در مورد درس, توضیحاتی در مورد درس, توضیحاتی در مورد درس, توضیحاتی در مورد درس',
                'content_type': Enumerations.objects.get(title='text').id,
                'file': None
            }, {
                'course_sub_section_item': 2,
                'content': None,
                'content_type': Enumerations.objects.get(title='image').id,
                'file': image_file.id
            }
        ]
        content = CourseSubSectionItemContentSerializer(data=content_data, many=True)
        content.is_valid()
        if content.errors:
            print(content.errors)
            return
        content.save()
        print('course_created')
