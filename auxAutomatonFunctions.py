import itertools


def unite_states(state1, state2, automaton):
    # Function that merges two states into a single new state
    alphabet = automaton[0]
    states = automaton[1]
    initial_state = automaton[2]
    final_states = automaton[3]
    productions = automaton[4]
    
    # Create new state
    new_state = state1 + state2

    # Update final states set if necessary
    if((state1 in final_states) or (state2 in final_states)):
        final_states.discard(state1)
        final_states.discard(state2)
        final_states.add(new_state)
    
    # Update initial state if necessary
    if((state1 in initial_state) or (state2 in initial_state)):
        initial_state.clear()
        initial_state.add(new_state)

    # Redirect all transitions going into or out of the original states to the new unified state
    for state in states:
        for symbol in alphabet:
            try:
                if (productions[state][symbol] == state1) or (productions[state][symbol] == state2):
                    productions[state][symbol] = new_state
            except:
                continue

    # Copy transitions to the new state
    productions[new_state] = dict(productions[state1])
    productions[new_state].update(productions[state2])

    # Delete original states transitions
    del productions[state1]
    del productions[state2]

    # Replace all states that are contained in new state with new state
    for i in range(len(states)):
        if states[i] in new_state:
            states[i] = new_state
    
    return states


def remove_useless_states(automaton):
    # An useless state is a state that is not final and can't reach any other state besides itself
    alphabet = automaton[0]
    states = automaton[1]
    initial_state = automaton[2]
    final_states = automaton[3]
    productions = automaton[4]
    useless_states = set()

    # Looks for useless states in the automaton
    for state in states:
        # If state is final state it's not useless
        if state not in final_states:
            useless = True
            for symbol in alphabet:
                try:
                    # If state can reach a state besides itself it's not useless
                    if productions[state][symbol] != state:
                        useless = False
                except:
                    continue

            if useless:
                useless_states.add(state)     

    # Delete all useless states and the productions that mention them
    for useless_state in useless_states:
        states.remove(useless_state)

        if useless_state in initial_state:
            initial_state.clear()

        for state in states:
            try:
                for symbol in alphabet:
                    if productions[state][symbol] == useless_state:
                        del productions[state][symbol]
            except:
                continue

        del productions[useless_state]
    
    return 


def get_reachables(state, productions, alphabet, reachables):
    # Gets the productions with state being the origin
    try:
        state_productions = productions[state]
    except:
        return 
    
    # Destiny set contains all the states reachable from state directly
    destiny = set()
    for symbol in alphabet:
        try:
            destiny.add(state_productions[symbol])
        except:
            continue
    
    # If one of the states reachable from the origin state is not in reachable...
    destinies = destiny - reachables
    if(len(destinies) > 0):
        # Add that state to the reachables set
        for destiny_state in destinies:
            reachables.add(destiny_state)

        # Call get_reachable recursively to check the reachable states starting from each added state
        for destiny_state in destinies:
            get_reachables(destiny_state,productions,alphabet,reachables)
    
    return


def remove_unreachable_states(automaton):
    alphabet = automaton[0]
    states = automaton[1]
    initial_state = list(automaton[2])[0]
    final_states = automaton[3]
    productions = automaton[4]

    # Recursively determine the states that can be reached starting from the initial state (similar to BFS)
    reachables = set(initial_state)
    get_reachables(initial_state,productions,alphabet, reachables)

    # Remove unreachable states from automaton
    states_set = set(states)
    non_reachables = states_set - reachables
    for state in non_reachables:
        if state in productions:
            del productions[state]

        states.remove(state)
        final_states.discard(state)
    return


def complete_automaton(automaton):
    # Makes the program function of the automaton total (dump state for non existent productions)
    alphabet = automaton[0]
    states = automaton[1]
    productions = automaton[4]
    added_dump_state = False
    
    # Initializes dump state with a name that is not already a name of a state
    dump_state = 'D'
    while(dump_state in states):
        dump_state = chr(ord(dump_state) + 1)
    
    # Checks for non-determined productions
    for state in states:
        for symbol in alphabet:
            try:
                productions[state][symbol]
            except:
                # adding dump state to the automaton if needed
                if(not added_dump_state):
                    aux_dict = {}
                    # dump state loops to itself for every possible symbol
                    for symbol_dump in alphabet:
                        transition = symbol_dump
                        destiny = dump_state
                        aux_dict[transition] = destiny
                    productions[dump_state] = aux_dict
                    added_dump_state = True
                
                # non-determined production is now a production with dump_state as destiny
                productions[state][symbol] = dump_state

    if added_dump_state:
        states.append(dump_state)
    return 


def print_automaton(automaton):
    alphabet = automaton[0]
    states = automaton[1]
    initial_state = automaton[2]
    final_states = automaton[3]
    productions = automaton[4]

    # Print alphabet
    if(len(alphabet) > 0):
        print("\nAlphabet:", alphabet)
    else:
        print("\nAlphabet: " + '\u2205')

    # Print states
    if(len(states) > 0):
        print("States:", set(states))
    else:
        print("States: " + '\u2205')

    # Print initial state
    if(len(initial_state) > 0):
        print("Initial State:", initial_state)
    else:
        print("Initial State: " + '\u2205')

    # Print final states
    if(len(final_states) > 0):
        print("Final States:", final_states)
    else:
        print("Final States: " + '\u2205')

    # Print productions
    print("Productions:")
    for state in states:
        for symbol in alphabet:
            try:
                next_state = productions[state][symbol]
                print(f"  δ({state},{symbol}) = {next_state}")
            except:
                continue
    return


def combinations(alphabet, word_length):
    #  Function that given an alphabet and a word length, generates all possible words
    # with word_length characters using the alphabet symbols
    generator = itertools.product(*([alphabet] * word_length)) 
    return [''.join(combination) for combination in generator]