class PDA:
    def __init__(self, variables, terminals, start_variable, production_rules):
        self.states = ['q_start', 'q_push_start_var', 'q_loop', 'q_final']
        self.variables = variables
        self.terminals = terminals
        self.start_variable = start_variable
        self.production_rules = production_rules
        self.transitions = self.create_transitions()

    def create_transitions(self):
        transitions = {}
        epsilon = 'ε'

        # Transition from q_start to q_push_start_var, pushing the stack symbol $
        transitions[('q_start', epsilon, epsilon)] = [('q_push_start_var', '$')]

        # Transition from q_push_start_var to q_loop, pushing the start variable
        transitions[('q_start_var', epsilon, epsilon)] = [('q_loop', self.start_variable)]

        # Transitions for production rules, in q_loop state
        state_counter = 1

        for variable in self.variables:
            for prod_rule in self.production_rules[variable]:
                previous_state = 'q_loop'
                for idx, symbol in enumerate(prod_rule[::-1]):
                    new_state = f'q_alt_{state_counter}'
                    state_counter += 1
                    transitions[(previous_state, epsilon, variable)] = [(new_state, symbol)]
                    previous_state = new_state
                    variable = epsilon  # Clear the variable after the first iteration

                # Transition back to q_loop after pushing all symbols
                transitions[(previous_state, epsilon, epsilon)] = [('q_loop', epsilon)]

        # Transitions for terminal symbols, in q_loop state
        for terminal in self.terminals:
            # For each terminal symbol a, with input a and pop a, push ε
            transitions[('q_loop', terminal, terminal)] = [('q_loop', epsilon)]

        # Transition from q_loop to q_final, popping the stack symbol $
        transitions[('q_loop', epsilon, '$')] = [('q_final', epsilon)]

        return transitions

def main():
    variables = {'S', 'B'}
    terminals = {'a', 'b', 'c'}
    start_variable = 'S'
    production_rules = {
        'S': ['aBc', 'ab'],
        'B': ['SB', 'ε']
    }

    pda = PDA(variables, terminals, start_variable, production_rules)
    
    for key, values in pda.transitions.items():
        for value in values:
            print(f"From {key[0]} with input '{key[1]}' and pop '{key[2]}': to {value[0]} and push '{value[1]}'")
    print(f"")
    print(f"another format\n")
    for key, values in pda.transitions.items():
        for value in values:
            print(f"δ({key[0]}, {key[1]}, {key[2]}) = ({value[0]}, {value[1]})")

if __name__ == '__main__':
    main()