from enum import Enum


class CourseStatusEnums(Enum):
    parent = 10
    ACTIVE = 11
    INACTIVE = 12

    @staticmethod
    def parent_name():
        return 'course_status'
