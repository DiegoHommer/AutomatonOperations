import auxAutomatonFunctions
import readAutomaton
import opsAutomaton

# Initialization by asking for input automaton and minimizing it
automaton_definition = -1
while(automaton_definition == -1):
    print(" Input the path to the file that defines the DFA")
    file_path = input()
    automaton_definition = readAutomaton.read_file(file_path)
minimized_automaton = readAutomaton.read_automaton(automaton_definition)
original_automaton = readAutomaton.read_automaton(automaton_definition)
opsAutomaton.minimize_automaton(minimized_automaton)




# Operations Menu
while(True):
    print("\n Choose an option!")
    print(" [1] - Change automaton being operated upon")
    print(" [2] - Display original automaton")
    print(" [3] - Display minimized automaton")
    print(" [4] - Display accepted words from a given list")
    print(" [5] - Display if automaton language is empty")
    print(" [6] - Exit program")
    option = int(input())
    
    if option == 1:
        # Change input automaton option
        automaton_definition = -1
        while(automaton_definition == -1):
            print(" Input the path to the file that defines the DFA")
            file_path = input()
            automaton_definition = readAutomaton.read_file(file_path)
        minimized_automaton = readAutomaton.read_automaton(automaton_definition)
        original_automaton = readAutomaton.read_automaton(automaton_definition)
        opsAutomaton.minimize_automaton(minimized_automaton)

    elif option == 2:
        # Display original automaton option
        auxAutomatonFunctions.print_automaton(original_automaton)

    elif option == 3:
        # Display minimized automaton option
        auxAutomatonFunctions.print_automaton(minimized_automaton)

    elif option == 4:
        # Check accepted words from word list option
        word_list = -1
        while(word_list == -1):
            print(" Input the path to the file with the list of words to be tested:")
            word_list_path = input()
            word_list = readAutomaton.read_file(word_list_path)
        word_list = word_list.replace(' ', '')
        word_list = word_list.replace('\n', '')
        word_list = word_list.split(',')
        accepted = opsAutomaton.simulate_automaton(minimized_automaton, word_list)
        print("\nAccepted Words:")
        for word in accepted:
            print(word)

    elif option == 5:
        # Check empty language option
        empty = opsAutomaton.check_empty_language(minimized_automaton)
        if(empty):
            print("\n The automaton language is empty!")
        else:
            print("\n The automaton language is not empty!")

    elif option == 6:
        # End program option
        break







