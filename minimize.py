
def create_automaton(alphabet_list, states_list, initial_state, final_states_list, productions_list):
    states={'q0', 'q1', 'q2','q3'},
    input_symbols={'a', 'b'},
    transitions={
        'q0': {'a': 'q1', 'b': 'q3'},
        'q1': {'a': 'q0', 'b': 'q2'},
        'q2': {'a': 'q2', 'b': 'q1'},
    },
    initial_state='q0',
    final_states={'q1'}
