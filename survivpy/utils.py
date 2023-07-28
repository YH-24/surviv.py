from .enums import *


def string_enum(name, enum_object, default):
    try:
        enum = enum_object.__getattr__(str(name).title())
    except AttributeError:
        enum = default

    return enum
