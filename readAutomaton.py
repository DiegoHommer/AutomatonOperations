import numpy as np

def read_file(file_name):
    file = open(file_name,'r')
    file_strings = file.readlines()
    file.close()
    stringao = ''.join(file_strings)
    return stringao

def read_automaton(stringao):
    # Reading automata name
    automata_name = stringao[0:stringao.find('=')]
    stringao = stringao.removeprefix(automata_name + '={ {')       


    # Extracting the automaton alphabet from file string
    alphabet_string = stringao[0:stringao.find('}')]
    alphabet_set = set(alphabet_string.split(', '))
    stringao = stringao.removeprefix(alphabet_string + '}, {')     
    stringao = stringao.removeprefix(alphabet_string + '},\n{')    


    # Extracting the automaton states from file string
    states_string = stringao[0:stringao.find('}')]
    states_set = set(states_string.split(', '))
    stringao = stringao.removeprefix(states_string + '}, ')     
    stringao = stringao.removeprefix(states_string + '},\n') 

    # Extracting the automaton initial state from file string
    initial_state_string = stringao[0:stringao.find(',')]
    initial_state = {initial_state_string}
    stringao = stringao.removeprefix(initial_state_string + ', {')


    # Extracting the automaton final states from file string
    final_states_string = stringao[0:stringao.find('}')]
    final_states_set = set(final_states_string.split(', '))
    stringao = stringao.removeprefix(final_states_string + '} }\np:\n')

    # Extracting the automaton productions from file string
    productions_list = stringao.split('\n')
    
    return (alphabet_set, states_set, initial_state, final_states_set, productions_list)