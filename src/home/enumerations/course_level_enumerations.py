from enum import Enum


class CourseLevelEnums(Enum):
    parent = 6
    EASY = 7
    MIDD = 8
    HARD = 9

    @staticmethod
    def parent_name():
        return 'course_levels'
