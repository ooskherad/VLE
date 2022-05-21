from enum import Enum


class ContentTypeEnums(Enum):
    parent = 1
    FILE = 2
    VIDEO = 3
    IMAGE = 4
    TEXT = 5

    @staticmethod
    def parent_name():
        return 'content_type'
