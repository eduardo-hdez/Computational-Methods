def epsilon_closure(states):
    stack = list(states)
    closure = set(states)

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
    start_state = epsilon_closure({nfa.start})
    dfa_transitions = {}
    queue = [start_state]
    visited = {start_state}

    while queue:
        current_state = queue.pop(0)

        for symbol in sorted(alphabet):
            next_states = epsilon_closure(move(current_state, symbol))

            if next_states:
                dfa_transitions[(current_state, symbol)] = next_states

                if next_states not in visited:
                    visited.add(next_states)
                    queue.append(next_states)

    accept_states = set()

    for state in visited:
        if nfa.accept in state:
            accept_states.add(state)

    return dfa_transitions, start_state, accept_states


def print_dfa(dfa_transitions, start_state, accept_states):
    state_names = {}
    name_counter = 0
    queue = [start_state]
    state_names[start_state] = chr(ord('A') + name_counter)
    name_counter += 1

    while queue:
        current_state = queue.pop(0)
        symbols = []

        for (state, symbol) in dfa_transitions:
            if state == current_state:
                symbols.append(symbol)

        symbols = sorted(symbols)

        for symbol in symbols:
            next_state = dfa_transitions[(current_state, symbol)]

            if next_state and next_state not in state_names:
                state_names[next_state] = chr(ord('A') + name_counter)
                name_counter += 1
                queue.append(next_state)

    print("\nDFA:")
    
    for state in sorted(state_names, key=lambda entry: state_names[entry]):
        symbols = []

        for (key_state, symbol) in dfa_transitions:
            if key_state == state:
                symbols.append(symbol)

        symbols = sorted(symbols)
        transitions = []

        for symbol in symbols:
            next_state = dfa_transitions.get((state, symbol))

            if next_state and next_state in state_names:
                transitions.append((state_names[next_state], symbol))

        if transitions:
            print(f"{state_names[state]} => {transitions}")

    accepting_names = []

    for state in accept_states:
        if state in state_names:
            accepting_names.append(state_names[state])

    accepting_names = sorted(accepting_names)
    print(f"Accepting states: {accepting_names}")


def accepts(dfa_transitions, start_state, accept_states, input_string):
    current_state = start_state

    for character in input_string:
        current_state = dfa_transitions.get(
            (current_state, character), frozenset()
        )

    return current_state in accept_states