from automata.fa.dfa import DFA
from white_box_oracle import WhiteBoxOracle
from user_input_oracle import UserInputOracle
from lstar import LStarAlgorithm
import time

def test_with_simple_dfa():
    """
    Test the L* algorithm with a simple DFA that accepts strings with an odd number of 1s.
    """
    print("\n=== Testing L* algorithm with a simple DFA ===")

    # Define a simple DFA that accepts strings with an odd number of 1s
    dfa = DFA(
        states={'q0', 'q1'},
        input_symbols={'0', '1'},
        transitions={
            'q0': {'0': 'q0', '1': 'q1'},
            'q1': {'0': 'q1', '1': 'q0'}
        },
        initial_state='q0',
        final_states={'q1'}
    )

    # Create an oracle for the DFA
    oracle = WhiteBoxOracle(dfa)

    # Create and run the L* algorithm
    lstar = LStarAlgorithm({'0', '1'}, oracle)
    learned_dfa = lstar.run()

    # Print statistics
    stats = lstar.get_statistics()
    print(f"\nLearning completed with:")
    print(f"- {stats['membership_queries']} membership queries")
    print(f"- {stats['equivalence_queries']} equivalence queries")

    # Visualize the learned DFA
    learned_dfa.show_diagram(path="learned_simple_dfa.png")
    print("Learned DFA saved as 'learned_simple_dfa.png'")

    return learned_dfa

def test_with_angluin_paper_dfa():
    """
    Test the L* algorithm with the DFA from Angluin's paper.
    """
    print("\n=== Testing L* algorithm with Angluin's paper DFA ===")

    # Define the DFA from Angluin's paper
    angluin_paper_dfa = DFA(
        states={"q0", "q1", "q2", "q3"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q1", "1": "q2"},
            "q1": {"0": "q0", "1": "q3"},
            "q2": {"0": "q3", "1": "q0"},
            "q3": {"0": "q2", "1": "q1"},
        },
        initial_state="q0",
        final_states={"q0"},
    )

    # Create an oracle for the DFA
    oracle = WhiteBoxOracle(angluin_paper_dfa)

    # Create and run the L* algorithm
    lstar = LStarAlgorithm({'0', '1'}, oracle)
    learned_dfa = lstar.run()

    # Print statistics
    stats = lstar.get_statistics()
    print(f"\nLearning completed with:")
    print(f"- {stats['membership_queries']} membership queries")
    print(f"- {stats['equivalence_queries']} equivalence queries")

    # Visualize the learned DFA
    learned_dfa.show_diagram(path="learned_angluin_dfa.png")
    print("Learned DFA saved as 'learned_angluin_dfa.png'")

    return learned_dfa

def test_with_user_input():
    """
    Test the L* algorithm with user input as the oracle.
    This allows the user to define their own language and see if the algorithm can learn it.
    """
    print("\n=== Testing L* algorithm with user input ===")
    print("You will be asked to answer membership and equivalence queries.")
    print("For membership queries, enter 'y' if the string is in the language, 'n' otherwise.")
    print("For equivalence queries, enter 'y' if the hypothesis is correct, or a counterexample otherwise.")

    # Define the alphabet
    alphabet = input("Enter the alphabet symbols separated by spaces (e.g., '0 1'): ").split()

    # Create a dummy DFA for the UserInputOracle (it won't be used for actual queries)
    dummy_dfa = DFA(
        states={'q0'},
        input_symbols=set(alphabet),
        transitions={'q0': {a: 'q0' for a in alphabet}},
        initial_state='q0',
        final_states=set()
    )

    # Create an oracle that uses user input
    oracle = UserInputOracle(dummy_dfa)

    # Override the membership_query_impl method to ask the user
    def membership_query_impl(self, word):
        while True:
            try:
                print(f"Is the string '{word}' in your language? (y/n)")
                user_input = input()
                if user_input.lower() == 'y':
                    return True
                elif user_input.lower() == 'n':
                    return False
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
            except:
                print("Invalid input. Please enter 'y' or 'n'.")

    # Replace the method in the oracle
    oracle.membership_query_impl = membership_query_impl.__get__(oracle, UserInputOracle)

    # Create and run the L* algorithm
    lstar = LStarAlgorithm(set(alphabet), oracle)
    learned_dfa = lstar.run()

    # Print statistics
    stats = lstar.get_statistics()
    print(f"\nLearning completed with:")
    print(f"- {stats['membership_queries']} membership queries")
    print(f"- {stats['equivalence_queries']} equivalence queries")

    # Visualize the learned DFA
    learned_dfa.show_diagram(path="learned_user_dfa.png")
    print("Learned DFA saved as 'learned_user_dfa.png'")

    return learned_dfa

if __name__ == "__main__":
    print("L* Algorithm Test Suite")
    print("=======================")

    while True:
        print("\nChoose a test to run:")
        print("1. Test with a simple DFA (odd number of 1s)")
        print("2. Test with Angluin's paper DFA")
        print("3. Test with user input")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            test_with_simple_dfa()
        elif choice == '2':
            test_with_angluin_paper_dfa()
        elif choice == '3':
            test_with_user_input()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
