import itertools
import auxAutomatonFunctions


def mark_dependencies(pair, dependencies, matrix, visited_pairs):
    return


# Function that given an automaton returns it's minimized version
def minimize_automaton(automaton):
    auxAutomatonFunctions.remove_unreachable_states(automaton)
    auxAutomatonFunctions.complete_automaton(automaton)

    alphabet = automaton[0]
    states = list(automaton[1])
    final_states = automaton[3]
    productions = automaton[4]

    matrix = [[[] for _ in range(len(states))] for _ in range(len(states))]
    dependencies = {pair: [] for pair in itertools.product(states, repeat=2)}


    # For all states p that are final states, mark the pairs {p, q} where q is not a final state
    for i in range(0,len(states)):
        if states[i] in final_states:
            for j in range(0,len(states)):
                if states[j] not in final_states:
                    matrix[i][j] = 1
    
    # For each pair {p, q} that wasnt marked before
    for i in range(0,len(states)):
        for j in range(0, len(states)):
            pair = (states[i],states[j])
            for symbol in alphabet:
                destiny1 = productions[pair[0]][symbol]
                destiny2 = productions[pair[1]][symbol]

                if matrix[states.index(destiny1)][states.index(destiny2)] == 1:
                    mark_dependencies((i,j), dependencies, matrix, set())
                else:
                    dependencies[(destiny1, destiny2)].append((i,j))
    
    return


#  Function that given an automaton M and a list of words, returns all the words from the list
# that belong to ACCEPT(M)
def simulate_automaton(automaton, word_list):
    alphabet = automaton[0]
    initial_state = automaton[2]
    final_states = automaton[3]
    productions = automaton[4]
    
    accepted_words = []

    # Simutating each word in word list running in automaton
    for word in word_list:
        state = initial_state
        accept = True
        
        for symbol in word:
            if symbol not in alphabet:
                # Invalid symbol -> REJECT
                accept = False
                break
            try:
                # Jumps to the next state if possible
                state = productions[state][symbol]
            except:
                # Indetermination -> REJECT
                accept = False
                break
        
        # Stopped on non final state -> REJECT
        if (state not in final_states):
            accept = False

        if accept:
            accepted_words.append(word)

    return(accepted_words)


# Functions that checks if the language that a given automaton recognizes is empty
def check_empty_language(automaton):
    alphabet = automaton[0]
    num_states = len(automaton[1])

    # Generates all possible words with length lesser than the number of states of the automaton
    for word_length in range (0,num_states):
        possible_words = auxAutomatonFunctions.combinations(alphabet, word_length)
        
        for word in possible_words:
            accepted_word = simulate_automaton(automaton, [word])
            # If one of the words generated was accepted, language is not empty language
            if accepted_word:
                return False
    
    # If all of the words tested were rejected, language is empty language
    return True