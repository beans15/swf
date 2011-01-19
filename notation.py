# -*- coding: utf-8 -*-


notation_table = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def convert_int_notation(value, base):
    """位取り記数法に基づき、数字を文字列に変換する
    >>> convert_int_notation(12, 2)
    '1100'
    >>> convert_int_notation(12, 8)
    '14'
    >>> convert_int_notation(31, 16)
    '1F'
    >>> convert_int_notation(0, 16)
    '0'
    >>> convert_int_notation(-31, 32)
    '-V'
    """
    if not 2 <= base <= 36:
        raise ValueError("Argument 'base' must be in 2 to 36.")

    if value == 0:
        return str(value)

    _value = value
    value = abs(value)
    result = []
    while value > 0:
        result.append(notation_table[value % base])
        value = int(value // base)

    if _value < 0:
        result.append('-')

    return ''.join(reversed(result))


def fill_characters_to_head(string, digit, char='0'):
    """先頭に指定した文字を埋めることで、指定した桁数にする
    >>> fill_characters_to_head('110', 4)
    '0110'
    """
    return char * max(digit - len(string), 0) + string


def convert_byte_to_bin(value):
    """8ビットの数字を2進数に変換し、8桁にする"""
    return fill_characters_to_head(convert_int_notation(value, 2), 8)
