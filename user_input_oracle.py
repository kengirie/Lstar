from automata.fa.dfa import DFA
from abstract_oracle import AbstractOracle
from overrides import overrides

class UserInputOracle(AbstractOracle):

    @overrides
    def equivalence_query_impl(self, hypothesis):
        while True:
            try:
                print("Enter 'y' if the hypothesis is correct, 'n' otherwise.")
                print("Hypothesis: ")
                hypothesis.show_diagram()
                user_input = input()
                if user_input == 'y':
                    return True
                elif user_input == 'n':
                    print("Enter a counterexample:")
                    counterexample = input()
                    return counterexample
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
            except:
                print("Invalid input. Please enter 'y' or 'n'.")

    @overrides
    def membership_query_impl(self, word):
        return self.target.accepts_input(word)
