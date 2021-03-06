"""
Этот модуль предоставляет несколько функций манипулирования строками.
>> s_balanced("(Python (is (not (lisp))))")
True
>> shorten('The Crossing', 10)
'The Cro...'
>> simplify(" some text with spurious whitespace ")
'some text with spurious whitespace'
"""
import string

def simplify(text, whitespace=string.whitespace, delete=''):
    r"""Возвращает текст, из которого удалены лишние пробелы.
    >>> simplify(" this    and\n that\t too")
    'this and that too'
    >>> simplify("  Washington   D.C.\n")
    'Washington D.C.'
    >>> simplify("  Washington   D.C.\n", delete=",;:.")
    'Washington DC'
    >>> simplify(" disemvoweled ", delete="aeiou")
    'dsmvwld'
    """
    result = []
    word = ''
    for char in text:
        if char in delete:
            continue
        elif char in whitespace:
            if word:
                result.append(word)
                word = ''
        else:
            word += char
    if word:
        result.append(word)
    return ' '.join(result)





def is_balanced(text, brackets='()[]{}<>'):
    counts = {}
    left_for_right = {}
    for left, right in zip(brackets[::2], brackets[1::2]):
        assert left != right, 'the vracket characters must differ'
        counts[left] = 0
        left_for_right[right] = left
    for c in text:
        if c in counts:
            counts[c] += 1
        elif c in left_for_right:
            left = left_for_right[c]
            if counts[left] == 0:
                return False
            counts[left] -= 1
    return not any(counts.values())

if __name__ == '__main__':
    import doctest
    doctest.testmod()