# -*- coding: utf-8 -*-

from datatypes import RGB, String, Rect, RGBA
from itertools import islice
from struct import unpack


def get_tag_class_for_type(tag_type):
    try:
        return dict(TAGS)[tag_type]
    except KeyError:
        return NotImplementedTag


TAG_PLACE_OBJECT = 4
TAG_PLACE_OBJECT2 = 26
TAG_PLACE_OBJECT3 = 70
TAG_REMOVE_OBJECT = 5
TAG_REMOVE_OBJECT2 = 28
TAG_SHOW_FRAME = 1
TAG_SET_BACKGROUND_COLOR = 9
TAG_FRAME_LABEL = 43
TAG_PROTECT = 24
TAG_END = 0
TAG_EXPORT_ASSETS = 56
TAG_IMPORT_ASSETS = 57
TAG_ENABLE_DEBUGGER = 58
TAG_ENABLE_DEBUGGER2 = 64
TAG_SCRIPT_LIMITS = 65
TAG_SET_TAB_INDEX = 66
TAG_FILE_ATTRIBUTES = 69
TAG_IMPORT_ASSETS2 = 71
TAG_SYMBOL_CLASS = 76
TAG_METADATA = 77
TAG_DEFINE_SCALING_GRID = 78
TAG_DEFINE_SCENE_AND_FRAME_LABEL_DATA = 86
TAG_DO_ACTION = 12
TAG_DO_INIT_ACTION = 59
TAG_DO_ABC = 82
TAG_DEFINE_SHAPE = 2
TAG_DEFINE_SHAPE2 = 22
TAG_DEFINE_SHAPE3 = 32
TAG_DEFINE_SHAPE4 = 83
TAG_DEFINE_BITS = 6
TAG_JPEG_TABLES = 8
TAG_DEFINE_BITS_JPEG2 = 21
TAG_DEFINE_BITS_JPEG3 = 35
TAG_DEFINE_BITS_LOSSLESS = 20
TAG_DEFINE_BITS_JPEG4 = 90
TAG_DEFINE_MORTH_SHAPE = 46
TAG_DEFINE_MORTH_SHAPE2 = 84
TAG_DEFINE_FONT = 10
TAG_DEFINE_FONT_INFO = 13
TAG_DEFINE_FONT_INFO2 = 62
TAG_DEFINE_FONT2 = 48
TAG_DEFINE_FONT3 = 75
TAG_DEFINE_FONT_ALIGN_ZONES = 73
TAG_DEFINE_FONT_NAME = 88
TAG_DEFINE_TEXT = 11
TAG_DEFINE_TEXT2 = 33
TAG_DEFINE_EDIT_TEXT = 37


class BaseTag(object):
    def __init__(self, data):
        pass


#-------------#
# General Tag #
#-------------#
class NotImplementedTag(BaseTag):
    def __init__(self, data):
        raise NotImplementedError()


class EmptyTag(BaseTag):
    def __init__(self, data):
        pass


def simple_tag_factory(*fields):
    """Create a class to analyze the content of tag
    which is made of simple fields, byte, integer, String.
    This function does not support variable count fields.

    Args:
        *fields: Tuples of (field_name, datatype_class).
                 ``field_name`` is an attribute name set to the instance.
                 ``datatype_class`` is descendant of BaseDataType class or
                 tuple of (unpacking format, byte length).

    Returns:
        A class to analyze the content of tag.
    """
    class _SimpleTag(BaseTag):
        def __init__(self, data):
            data = iter(data)
            for field_name, datatype_class in fields:
                if isinstance(datatype_class, tuple):
                    # ``datatype_class`` is (format, bytes)
                    fmt, byte_count = datatype_class
                    value = unpack(fmt, ''.join(islice(data, byte_count)))[0]
                    setattr(self, field_name, value)
                else:
                    setattr(self, field_name, datatype_class(data))
    return _SimpleTag


#------------#
# Unique Tag #
#------------#
class FileAttributesTag(BaseTag):
    def __init__(self, data):
        data = iter(data)
        flags = ord(next(data))
        self.reserved1 = bool(flags & 128)
        self.use_direct_blit = bool(flags & 64)
        self.use_gpu = bool(flags & 32)
        self.has_metadata = bool(flags & 16)
        self.action_script3 = bool(flags & 8)
        self.reserved2 = bool(flags & 6)
        self.use_netword = bool(flags & 1)

        self.reserved3 = unpack('H', next(data) + next(data)) << 8 \
                             + ord(next(data))


class DefineEditTextTag(BaseTag):
    def __init__(self, data):
        data = iter(data)
        self.character_id = unpack('<H', ''.join(islice(data, 2)))[0]
        self.bounds = Rect(data)

        flags = ord(next(data))
        self.has_text = bool(flags & 128)
        self.word_wrap = bool(flags & 64)
        self.multiline = bool(flags & 32)
        self.password = bool(flags & 16)
        self.read_only = bool(flags & 8)
        self.has_text_color = bool(flags & 4)
        self.has_max_length = bool(flags & 2)
        self.has_font = bool(flags & 1)

        flags = ord(next(data))
        self.has_font_class = bool(flags & 128)
        self.auto_size = bool(flags & 64)
        self.has_layout = bool(flags & 32)
        self.no_select = bool(flags & 16)
        self.border = bool(flags & 8)
        self.was_static = bool(flags & 4)
        self.html = bool(flags & 2)
        self.use_outlines = bool(flags & 1)

        self.font_id = unpack('<H', ''.join(islice(data, 2)))[0] \
                           if self.has_font else None
        self.font_class = String(data) if self.has_font_class else None
        self.font_height = unpack('<H', ''.join(islice(data, 2)))[0] \
                               if self.has_font else None
        self.text_color = RGBA(data) if self.has_text_color else None
        self.max_length = unpack('<H', ''.join(islice(data, 2)))[0] \
                              if self.has_max_length else None
        self.align = ord(next(data)) if self.has_layout else None
        self.left_margin = unpack('<H', ''.join(islice(data, 2)))[0] \
                               if self.has_layout else None
        self.right_margin = unpack('<H', ''.join(islice(data, 2)))[0] \
                                if self.has_layout else None
        self.indent = unpack('<H', ''.join(islice(data, 2)))[0] \
                          if self.has_layout else None
        self.leading = unpack('<h', ''.join(islice(data, 2)))[0] \
                           if self.has_layout else None
        self.variable_name = String(data)
        self.initial_text = String(data) if self.has_text else None


#------------------#
# Tag type and Tag #
#------------------#
TAGS = (
    (TAG_PLACE_OBJECT, NotImplementedTag),
    (TAG_PLACE_OBJECT2, NotImplementedTag),
    (TAG_PLACE_OBJECT3, NotImplementedTag),
    (TAG_REMOVE_OBJECT,
        simple_tag_factory(('character_id', ('H', 2)),
                           ('depth', ('H', 2)))),
    (TAG_REMOVE_OBJECT2,
        simple_tag_factory(('depth', ('H', 2)))),
    (TAG_SHOW_FRAME, EmptyTag),
    (TAG_SET_BACKGROUND_COLOR,
        simple_tag_factory(('background_color', RGB))),
    (TAG_FRAME_LABEL,
        simple_tag_factory(('name', String),
                           ('name_anchor_flag', ('B', 1)))),
    (TAG_PROTECT, EmptyTag),
    (TAG_END, EmptyTag),
    (TAG_EXPORT_ASSETS, NotImplementedTag),
    (TAG_IMPORT_ASSETS, NotImplementedTag),
    (TAG_ENABLE_DEBUGGER,
        simple_tag_factory(('password', String))),
    (TAG_ENABLE_DEBUGGER2,
        simple_tag_factory(('reserved', ('H', 2)),
                           ('password', String))),
    (TAG_SCRIPT_LIMITS,
        simple_tag_factory(('max_recursion_depth', ('H', 2)),
                           ('script_timeout_seconds', ('H', 2)))),
    (TAG_SET_TAB_INDEX,
        simple_tag_factory(('depth', ('H', 2)),
                           ('tab_index', ('H', 2)))),
    (TAG_FILE_ATTRIBUTES, FileAttributesTag),
    (TAG_IMPORT_ASSETS2, NotImplementedTag),
    (TAG_SYMBOL_CLASS, NotImplementedTag),
    (TAG_METADATA,
        simple_tag_factory(('metadata', String))),
    (TAG_DEFINE_SCALING_GRID,
        simple_tag_factory(('character_id', ('H', 2)),
                           ('splitter', Rect))),
    (TAG_DEFINE_SCENE_AND_FRAME_LABEL_DATA, NotImplementedTag),
    (TAG_DO_ACTION, NotImplementedTag),
    (TAG_DO_INIT_ACTION, NotImplementedTag),
    (TAG_DO_ABC, NotImplementedTag),
    (TAG_DEFINE_SHAPE, NotImplementedTag),
    (TAG_DEFINE_SHAPE2, NotImplementedTag),
    (TAG_DEFINE_SHAPE3, NotImplementedTag),
    (TAG_DEFINE_SHAPE4, NotImplementedTag),
    (TAG_DEFINE_BITS, NotImplementedTag),
    (TAG_JPEG_TABLES, NotImplementedTag),
    (TAG_DEFINE_BITS_JPEG2, NotImplementedTag),
    (TAG_DEFINE_BITS_JPEG3, NotImplementedTag),
    (TAG_DEFINE_BITS_LOSSLESS, NotImplementedTag),
    (TAG_DEFINE_BITS_JPEG4, NotImplementedTag),
    (TAG_DEFINE_MORTH_SHAPE, NotImplementedTag),
    (TAG_DEFINE_MORTH_SHAPE2, NotImplementedTag),
    (TAG_DEFINE_FONT, NotImplementedTag),
    (TAG_DEFINE_FONT_INFO, NotImplementedTag),
    (TAG_DEFINE_FONT_INFO2, NotImplementedTag),
    (TAG_DEFINE_FONT2, NotImplementedTag),
    (TAG_DEFINE_FONT3, NotImplementedTag),
    (TAG_DEFINE_FONT_ALIGN_ZONES, NotImplementedTag),
    (TAG_DEFINE_FONT_NAME, NotImplementedTag),
    (TAG_DEFINE_TEXT, NotImplementedTag),
    (TAG_DEFINE_TEXT2, NotImplementedTag),
    (TAG_DEFINE_EDIT_TEXT, DefineEditTextTag),
)
