from enum import Enum


class GroupFileEnums(Enum):
    parent = 13
    COURSE_FILES = 14
    COURSE_CONTENTS = 15
    USER_PROFILE = 16

    @staticmethod
    def parent_name():
        return 'group_files'
