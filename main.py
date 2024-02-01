import numpy as np
import readAutomaton
import opsAutomaton


print("Forneça o path para o arquivo que descreve o AFD:")
file_path = input()
print("Forneça o path para o arquivo que contém a lista de palavras a serem testadas")
word_list_path = input()

automaton_definition = readAutomaton.read_file(file_path)
word_list = readAutomaton.read_file(word_list_path)
word_list = word_list.split(',')
automaton = readAutomaton.read_automaton(automaton_definition)
accepted = opsAutomaton.simulate_automaton(automaton, word_list)
empty = opsAutomaton.check_empty_language(automaton)
opsAutomaton.minimize_automaton(automaton)






