def epsilon_closure(states):
    stack, closure = list(states), set(states)
    while stack:
        state = stack.pop()
        for next_state in state.epsilon:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return frozenset(closure)

def move(states, symbol):
    reachable = set()
    for state in states:
        reachable |= set(state.transitions.get(symbol, []))
    return reachable

def nfa_to_dfa(nfa, alphabet):
    start = epsilon_closure({nfa.start})
    dfa_transitions = {}
    queue = [start]
    visited = {start}

    while queue:
        current = queue.pop(0)
        for symbol in sorted(alphabet):
            next_states = epsilon_closure(move(current, symbol))
            if next_states:
                dfa_transitions[(current, symbol)] = next_states
                if next_states not in visited:
                    visited.add(next_states)
                    queue.append(next_states)

    accept_states = {s for s in visited if nfa.accept in s}
    return dfa_transitions, start, accept_states

def print_dfa(dfa_transitions, start, accept_states):
    state_names = {}
    counter = 0
    queue = [start]
    state_names[start] = chr(ord('A') + counter)
    counter += 1

    while queue:
        current = queue.pop(0)
        symbols = sorted(sym for (s, sym) in dfa_transitions if s == current)
        for symbol in symbols:
            next_state = dfa_transitions[(current, symbol)]
            if next_state and next_state not in state_names:
                state_names[next_state] = chr(ord('A') + counter)
                counter += 1
                queue.append(next_state)

    print("\nDFA:")
    for state in sorted(state_names, key=lambda s: state_names[s]):
        symbols = sorted(sym for (s, sym) in dfa_transitions if s == state)
        trans = []
        for symbol in symbols:
            next_state = dfa_transitions.get((state, symbol))
            if next_state and next_state in state_names:
                trans.append((state_names[next_state], symbol))
        if trans:
            print(f"{state_names[state]} => {trans}")

    acc = sorted(state_names[s] for s in accept_states if s in state_names)
    print(f"Accepting states: {acc}")

def accepts(dfa_transitions, start, accept_states, string):
    current = start
    for character in string:
        current = dfa_transitions.get((current, character), frozenset())
    return current in accept_states