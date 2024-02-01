import itertools

def remove_unreachable_states(automaton):
    alphabet = automaton[0]
    states = automaton[1]
    initial_state = automaton[2]
    final_states = automaton[3]
    productions = automaton[4]

    reachables = set(initial_state)
    get_reachables(initial_state,productions,alphabet, reachables)

    non_reachables = states - reachables
    for state in non_reachables:
        if state in productions:
            del productions[state]

        states.discard(state)
        final_states.discard(state)
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
    
    
# Make the program function of the automaton total (dump state for non existent productions)
def complete_automaton(automaton):
    alphabet = automaton[0]
    states = automaton[1]
    productions = automaton[4]
    add_dump_state = True
    
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
                if(add_dump_state):
                    aux_dict = {}
                    # dump state loops to itself for every possible symbol
                    for symbol_dump in alphabet:
                        transition = symbol_dump
                        destiny = dump_state
                        aux_dict[transition] = destiny
                    productions[dump_state] = aux_dict
                    add_dump_state = False
                
                # non-determined production is now a production with dump_state as destiny
                productions[state][symbol] = dump_state

    states.add(dump_state)
    return 


#  Function that given an alphabet and a word length, generates all possible words
# with word_length characters using the alphabet symbols
def combinations(alphabet, word_length):
    generator = itertools.product(*([alphabet] * word_length)) 
    return [''.join(combination) for combination in generator]