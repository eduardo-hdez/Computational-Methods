class State:
    _id_counter = 0

    def __init__(self):
        self.id = State._id_counter
        State._id_counter += 1
        self.transitions = {}
        self.epsilon = []


class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept


def build_nfa(postfix):
    State._id_counter = 0
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


def print_nfa(nfa):
    visited = set()
    queue = [nfa.start]
    visited.add(nfa.start)

    while queue:
        state = queue.pop(0)

        for targets in state.transitions.values():
            for target in targets:
                if target not in visited:
                    visited.add(target)
                    queue.append(target)

        for target in state.epsilon:
            if target not in visited:
                visited.add(target)
                queue.append(target)

    states = sorted(visited, key=lambda state: state.id)

    print("\nNFA:")

    for state in states:
        transitions = []

        for symbol, targets in state.transitions.items():
            for target in targets:
                transitions.append((target.id, symbol))

        for target in state.epsilon:
            transitions.append((target.id, '#'))

        if transitions:
            print(f"{state.id} => {transitions}")

    print(f"Accepting state: {nfa.accept.id}")