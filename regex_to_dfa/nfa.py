class State:
    def __init__(self):
        self.transitions = {}
        self.epsilon = []

class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

def build_nfa(postfix):
    stack = []

    for character in postfix:
        if character == '.':
            right, left = stack.pop(), stack.pop()
            left.accept.epsilon.append(right.start)
            stack.append(NFA(left.start, right.accept))

        elif character == '|':
            right, left = stack.pop(), stack.pop()
            start, accept = State(), State()
            start.epsilon.append(left.start)
            start.epsilon.append(right.start)
            left.accept.epsilon.append(accept)
            right.accept.epsilon.append(accept)
            stack.append(NFA(start, accept))

        elif character == '*':
            current = stack.pop()
            start, accept = State(), State()
            start.epsilon.append(current.start)
            start.epsilon.append(accept)
            current.accept.epsilon.append(current.start)
            current.accept.epsilon.append(accept)
            stack.append(NFA(start, accept))

        elif character == '+':
            current = stack.pop()
            start, accept = State(), State()
            start.epsilon.append(current.start)
            current.accept.epsilon.append(current.start)
            current.accept.epsilon.append(accept)
            stack.append(NFA(start, accept))

        elif character == '?':
            current = stack.pop()
            start, accept = State(), State()
            start.epsilon.append(current.start)
            start.epsilon.append(accept)
            current.accept.epsilon.append(accept)
            stack.append(NFA(start, accept))

        else:
            start, accept = State(), State()
            start.transitions[character] = [accept]
            stack.append(NFA(start, accept))

    return stack[0]