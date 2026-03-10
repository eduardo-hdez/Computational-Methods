PRECEDENCE = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1}

def shunting_yard(regex):
    output, operators = [], []

    for character in regex:
        if character == "(":
            operators.append(character)

        elif character == ")":
            while operators and operators[-1] != "(":
                output.append(operators.pop())
            operators.pop()

        elif character in PRECEDENCE:
            while (operators and
                   operators[-1] != "(" and
                   operators[-1] in PRECEDENCE and
                   PRECEDENCE[operators[-1]] >= PRECEDENCE[character]):
                output.append(operators.pop())
            operators.append(character)

        else:
            output.append(character)

    while operators:
        output.append(operators.pop())
        
    return ''.join(output)