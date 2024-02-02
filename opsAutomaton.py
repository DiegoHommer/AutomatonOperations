import auxAutomatonFunctions
import copy

def mark_dependencies(index_pair, dependency_matrix, equivalence_matrix):
    # Mark the pair itself
    equivalence_matrix[index_pair[0]][index_pair[1]] = 1
    equivalence_matrix[index_pair[1]][index_pair[0]] = 1

    # And all the pairs that depended on it's equivalence to be equivalent
    for dependencie_pair in dependency_matrix[index_pair[0]][index_pair[1]]:
        if(equivalence_matrix[dependencie_pair[0]][dependencie_pair[1]] == 0):
            mark_dependencies(dependencie_pair,dependency_matrix,equivalence_matrix)

    # And all the pairs that depended on it's equivalence to be equivalent
    for dependencie_pair in dependency_matrix[index_pair[1]][index_pair[0]]:
        if(equivalence_matrix[dependencie_pair[0]][dependencie_pair[1]] == 0):
            mark_dependencies(dependencie_pair,dependency_matrix,equivalence_matrix)

    # Remove the dependencies after marking
    dependency_matrix[index_pair[0]][index_pair[1]] = []
    dependency_matrix[index_pair[1]][index_pair[0]] = []


def minimize_automaton(automaton):
    # Function that given an automaton returns it's minimized version

    # Step 0: Initialization for algorithm to work
    auxAutomatonFunctions.remove_unreachable_states(automaton)
    auxAutomatonFunctions.complete_automaton(automaton)

    alphabet = automaton[0]
    states = copy.deepcopy(automaton[1])
    initial_state = automaton[2]
    final_states = automaton[3]
    productions = automaton[4]

    # Matrix for marking pairs that are not equivalent with 1
    equivalence_matrix = [[0 for j in range(len(states))] for i in range(len(states))]

    # Matrix for vectors representing dependencies
    dependency_matrix = [[set() for _ in range(len(states))] for _ in range(len(states))]

    # For all states p that are final states, mark the pairs {p, q} where q is not a final state
    for i in range(0,len(states)):
        if states[i] in final_states:
            for j in range(0,len(states)):
                if states[j] not in final_states:
                    equivalence_matrix[i][j] = 1
                    equivalence_matrix[j][i] = 1


    # For each pair {p, q} that wasnt marked before
    for p_index in range(0,len(states)):
        for q_index in range(0, len(states)):
            if((equivalence_matrix[p_index][q_index] == 0) and (p_index != q_index)):
                p = states[p_index]
                q = states[q_index]

                # For each pair of transitions for each symbol of the alphabet
                for symbol in alphabet:
                    r_index = states.index(productions[p][symbol])
                    s_index = states.index(productions[q][symbol])
                    
                    if equivalence_matrix[r_index][s_index] == 1:
                        #  If the equivalence of {p,q} depends on a non-equivalent pair of states {r,s}
                        # {p,q} and all the pairs that depend on it to be equivalent are not equivalent.
                        mark_dependencies((p_index,q_index), dependency_matrix, equivalence_matrix)
                        break
                    else:
                        # Else, {p,q} depend on the equivalence of the non marked state pair {r,s}
                        dependency_matrix[r_index][s_index].add((p_index,q_index))
                        dependency_matrix[s_index][r_index].add((p_index,q_index))

    # For each each pair of equivalent states, merge the pair into a single new state
    for i in range(len(states)):
        for j in range(len(states)):
            if((equivalence_matrix[i][j] == 0) and (states[i] != states[j])):   
                states = auxAutomatonFunctions.unite_states(states[i],states[j],automaton) 
                equivalence_matrix[i][j] = 1
                equivalence_matrix[j][i] = 1

    # Remove the repeated instances of new state
    states_set = set(states)
    states.clear()
    states.extend(states_set)


    auxAutomatonFunctions.remove_useless_states(automaton)
    return 


#  Function that given an automaton M and a list of words, returns all the words from the list
# that belong to ACCEPT(M)
def simulate_automaton(automaton, word_list):
    alphabet = automaton[0]
    initial_state = list(automaton[2])[0]
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