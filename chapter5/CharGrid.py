"""
This module provides functionality for writing characters on a grid.

The module provides functions for adding horizontal and vertical lines,
and for (optionally filled) rectangles, and for (optionally boxed) text.

All char arguments must be strings of length 1; these are guarded by
assertions. If out of range row or column values are given, the
appropriate exception, RowRangeError or ColumnRangeError will
be raised---use the RangeError exception if you want to catch either.

>>> resize(14, 50)
>>> add_rectangle(0, 0, *get_size())
>>> add_vertical_line(5, 10, 13)
>>> add_vertical_line(2, 9, 12, "!")
>>> add_horizontal_line(3, 10, 20, "+")
>>> add_rectangle(0, 0, 5, 5, "%")
>>> add_rectangle(5, 7, 12, 40, "#", True)
>>> add_rectangle(7, 9, 10, 38, " ")
>>> add_text(8, 10, "This is the CharGrid module")
>>> add_text(1, 32, "Pleasantville", "@")
>>> add_rectangle(6, 42, 11, 46, fill=True)
>>> render(False)
%%%%%*********************************************
%   %                           @@@@@@@@@@@@@@@  *
%   %                           @Pleasantville@  *
%   %     ++++++++++            @@@@@@@@@@@@@@@  *
%%%%%                                            *
*      #################################         *
*      #################################  ****   *
*      ##                             ##  ****   *
*      ## This is the CharGrid module ##  ****   *
* !    ##                             ##  ****   *
* !  | #################################  ****   *
* !  | #################################         *
*    |                                           *
**************************************************
"""
import sys
import subprocess

class RangeError(Exception): pass
class RowRangeError(RangeError): pass
class ColumnRangeError(RangeError): pass

_CHAR_ASSERT_TEMPLATE = ('char must be a single character: "{0}" '
                         'is too long')
_max_rows = 25
_max_columns = 80
_grid = []
_background_char = ' '

if sys.platform.startswith('wind'):
    def clear_screen():
        subprocess.call('cmd.exe', '/C', 'cls')
else:
    def clear_screen():
        subprocess.call(['clear'])

clear_screen.__doc__ = """Clears the screen using the \ 
underlying window system's screen command"""


def tests():
    import pprint
    resize(5,5,'X')
    pprint.pprint(_grid)


def char_at(row, column):
    """Возвращает символ на заданной позиции
    >>> char_at(0, 0)
    '%'
    >>> char_at(4, 11)
    ' '
    >>> char_at(32, 24)
    Traceback (most recent call last):
    ...
    RowRangeError
    """
    try:
        return _grid[row][column]
    except IndexError:
        if not 0 <= row <= _max_rows:
            raise RowRangeError()
        raise ColumnRangeError()


def resize(max_rows, max_columns, char=None):
    """Изменяет размер сетки, очищает содержимое иизменяет символ фона,
    если аргумент char не равен None
    """
    assert max_rows > 0 and max_columns > 0, 'too small'
    global _grid, _max_rows, _max_columns, _background_char
    if char is not None:
        assert len(char) == 1, _CHAR_ASSERT_TEMPLATE.format(char)
        _background_char = char
    _max_rows = max_rows
    _max_columns = max_columns
    _grid = [[_background_char for column in range(_max_columns)] for row in range(_max_rows)]


def set_background(char=' '):
    """Устанавливает фоновый символ
    >>> set_background('$')
    >>> char_at(0, 0)
    '%'
    >>> char_at(4, 11)
    ' '
    >>> set_background('<>')
    Traceback (most recent call last):
    ...
    AssertionError: char must be a single character: "<>" is too long
    >>> set_background(' ')
    """
    assert len(char) == 1, _CHAR_ASSERT_TEMPLATE.format(char)
    global _background_char
    old_background_char = _background_char
    for row in range(_max_rows):
        for column in range(_max_columns):
            if _grid[row][column] == old_background_char:
                _grid[row][column] = _background_char


def add_vertical_line(column, row0, row1, char='|'):
    """Добавляет вертикальную линию в сетку, используя заданный символ

    >>> add_vertical_line(5, 2, 10, '&')
    >>> char_at(2, 5) == char_at(3, 5) == '&'
    True
    >>> add_vertical_line(85, 1, 2)
    Traceback (most recent call last):
    ...
    ColumnRangeError
    """
    assert len(char) == 1, _CHAR_ASSERT_TEMPLATE.format(char)
    try:
        for row in range(row0, row1):
            _grid[row][column] = char
    except IndexError:
        if not 0 <= row <= _max_rows:
            raise RowRangeError()
        raise ColumnRangeError()




def add_horizontal_line(row, column0, column1, char='-'):
    """Добавляет в сетку горизонтальную линию, используя указанный символ
    >>> add_horizontal_line(8, 20, 25, '=')
    >>> char_at(8, 20) == char_at(8, 24) == '='
    True
    >>> add_horizontal_line(31, 11, 12)
    Traceback (most recent call last):
    ...
    RowRangeError
    """

    assert len(char) ==1, _CHAR_ASSERT_TEMPLATE.format(char)
    try:
        for column in range(column0, column1):
            _grid[row][column] = char
    except IndexError:
        if not 0 <= row <= _max_rows:
            raise RowRangeError()
        raise ColumnRangeError(0)


def add_rectangle(row0, column0, row1, column1, char='*', fill=False):
    """
    Создаёт прямоугольную область на сетке: залитый или нет

    >>> add_rectangle(10, 30, 14, 35, '^', True)
    >>> char_at(10, 30) == char_at(12, 32) == '^'
    True
    """
    if not fill:
        add_vertical_line(column0, row0, row1, char)
        add_vertical_line(column1 - 1, row0, row1, char)
        add_horizontal_line(row0, column0, column1, char)
        add_horizontal_line(row1 - 1, column0, column1, char)
    else:
        assert len(char) == 1, _CHAR_ASSERT_TEMPLATE.format(char)
        try:
            for row in range(row0, row1):
                for column in range(column0, column1):
                    _grid[row][column] = char
        except IndexError:
            if not 0<= row <= _max_rows:
                raise RowRangeError()
            raise ColumnRangeError()


def add_text(row, column, text, char=None):
    """
    Если char не None, рисует прямоугольник из данного символа с текстом внутри
    >>> add_text(6, 15, 'Alpha Beta')
    >>> char_at(6, 15) == 'A'
    True
    """
    try:
        if char is None:
            for i, column in enumerate(range(column, column + len(text))):
                _grid[row][column] = text[i]
        else:
            assert len(char) == 1, _CHAR_ASSERT_TEMPLATE.format(char)
            row0 = row
            row1 = row0 + 3
            column0 = column
            column1 = column0 + len(text) + 2
            add_rectangle(row0, column0, row1, column1, char)
            row = row0 + 1
            for i , column in enumerate(range(column0 + 1, column1 - 1)):
                _grid[row][column] = text[i]
    except IndexError:
        if not 0 <= row <= _max_rows:
            raise RowRangeError()
        raise ColumnRangeError()


def render(clear=True):
    """Отправляет сетку в консоль
    """
    if clear:
        clear_screen()
    for row in range(_max_rows):
        print(''.join(_grid[row]))
        for column in range(_max_columns):
            _grid[row][column] == _background_char

def get_size():
    return _max_rows, _max_columns


resize(_max_rows, _max_columns)


if __name__ == '__main__':
    import doctest
    doctest.testmod()