def read_input():
    # Read the alphabet symbols
    alphabet = input("Enter alphabet symbols (press '?' to finish): ").split()
    if '?' in alphabet:
        alphabet.remove('?')

    # Read the number of states
    num_states = int(input("Enter the number of states: "))

    # Initialize the transitions table
    transitions = {}
    accept_states = set()

    for state in range(num_states):
        transitions[state] = {symbol: None for symbol in alphabet}

    # Read transitions for each state and alphabet symbol
    for state in range(num_states):
        for symbol in alphabet:
            next_state = input(f"Transitions from state q{state} using symbol {symbol} (press '@' for lambda): ")
            if next_state != '@':
                transitions[state][symbol] = next_state
            else:
                next_state = input(f"Lambda transition from state q{state} using symbol {symbol} to: ")
                transitions[state][symbol] = next_state

        # Add lambda transition
        lambda_transition = input(f"Transitions from state q{state} using symbol @ (press '?' to finish): ")
        if lambda_transition != '?':
            transitions[state]['@'] = lambda_transition

        # Determine accept states
        accept = input(f"Is state q{state} an accept state? (yes/no): ").lower()
        if accept == 'yes':
            accept_states.add(state)

    return alphabet, transitions, accept_states

def print_table(table):
    for state, transitions in table.items():
        for symbol, next_state in transitions.items():
            if next_state:
                print(f"q{state}==={symbol}===>q{next_state}")

def epsilon_closure(states, transitions):
    closure = set(states)
    stack = list(states)

    while stack:
        state = stack.pop()
        epsilon_transitions = transitions[state]['@']
        for next_state in epsilon_transitions:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)

    return closure

def main():
    alphabet, nfa_table, nfa_accept_states = read_input()

    print("\nNFATable:")
    print_table(nfa_table)
    print("Accept states in NFA:", nfa_accept_states)

    # Convert NFATable to DFATable
    dfa_table = {}
    dfa_accept_states = set()
    dfa_states = []

    # Initialize the DFA with the epsilon closure of the start state of the NFA
    start_state = epsilon_closure([0], nfa_table)
    dfa_states.append(start_state)
    dfa_table[0] = {symbol: epsilon_closure([int(next_state)], nfa_table) for symbol, next_state in nfa_table[0].items()}

    # Construct the rest of the DFA
    i = 0
    while i < len(dfa_states):
        state = dfa_states[i]
        for symbol in alphabet:
            next_state = set()
            for nfa_state in state:
                nfa_transitions = nfa_table[nfa_state][symbol]
                if nfa_transitions:
                    next_state.update(epsilon_closure([int(s) for s in nfa_transitions], nfa_table))
            if next_state:
                if next_state not in dfa_states:
                    dfa_states.append(next_state)
                dfa_table[state][symbol] = next_state
        i += 1

    # Determine accept states in DFA
    for i, state in enumerate(dfa_states):
        if any(s in nfa_accept_states for s in state):
            dfa_accept_states.add(i)

    print("\nDFATable:")
    for i, state in enumerate(dfa_states):
        print(f"State q{i}:", state)
    print("Accept states in DFA:", dfa_accept_states)

if __name__ == "__main__":
    main()
