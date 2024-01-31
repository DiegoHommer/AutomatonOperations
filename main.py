import numpy as np
import readAutomaton

print("Forneça o path para o arquivo que descreve o AFD:")
file_path = input()
automaton_definition = readAutomaton.read_file(file_path)
automato = readAutomaton.read_automaton(automaton_definition)







