import itertools

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


#  Function that given an alphabet and a word length, generates all possible words
# with word_length characters using the alphabet symbols
def combinations(alphabet, word_length):
    generator = itertools.product(*([alphabet] * word_length)) 
    return [''.join(combination) for combination in generator]


# Functions that checks if the language that a given automaton recognizes is empty
def check_empty_language(automaton):
    alphabet = automaton[0]
    num_states = len(automaton[1])

    # Generates all possible words with length lesser than the number of states of the automaton
    for word_length in range (0,num_states):
        possible_words = combinations(alphabet, word_length)
        
        for word in possible_words:
            accepted_word = simulate_automaton(automaton, [word])
            # If one of the words generated was accepted, language is not empty language
            if accepted_word:
                return False
    
    # If all of the words tested were rejected, language is empty language
    return True