"""
add_concat.py
Author: Eduardo Hernández Alonso
"""

def add_concat(regex):
    result = []

    for i, c in enumerate(regex):
        result.append(c)

        if i + 1 < len(regex):
            left, right = c, regex[i + 1]
            left_ok = left not in "(|"
            right_ok = right not in ")|*+?"

            if left_ok and right_ok:
                result.append('.')

    return ''.join(result)