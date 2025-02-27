from automata.fa.dfa import DFA
from white_box_oracle import WhiteBoxOracle
from user_input_oracle import UserInputOracle
from lstar import LStarAlgorithm

def test_oracle_basics():
    """Test basic oracle functionality"""
    print("\n=== Testing Oracle Basics ===")

    # Define a simple DFA
    my_dfa = DFA(
        states={'q0', 'q1', 'q2'},
        input_symbols={'0', '1'},
        transitions={
            'q0': {'0': 'q0', '1': 'q1'},
            'q1': {'0': 'q0', '1': 'q2'},
            'q2': {'0': 'q2', '1': 'q1'}
        },
        initial_state='q0',
        final_states={'q1'}
    )

    # Define a slightly different DFA
    my_dfa2 = DFA(
        states={"q0", "q1", "q2"},
        input_symbols={"0", "1"},
        transitions={
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q0", "1": "q2"},
            "q2": {"0": "q2", "1": "q1"},
        },
        initial_state="q0",
        final_states={"q2"},
    )

    # Create an oracle for the first DFA
    oracle = WhiteBoxOracle(my_dfa)

    # Test membership queries
    print(f"Empty string in language: {oracle.membership_query('')}")
    print(f"'101' in language: {oracle.membership_query('101')}")
    print(f"'100' in language: {oracle.membership_query('100')}")

    # Test equivalence query
    result = oracle.equivalence_query(my_dfa2)
    print(f"DFAs equivalent: {result if result is True else 'No, counterexample: ' + str(result)}")

    # Print statistics
    print(f"Number of equivalence queries: {oracle.get_num_of_eq()}")
    print(f"Number of membership queries: {oracle.get_num_of_mq()}")

def test_angluin_paper_dfa():
    """Test the L* algorithm with the DFA from Angluin's paper"""
    print("\n=== Testing with Angluin's Paper DFA ===")

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

if __name__ == "__main__":
    print("L* Algorithm Tests")
    print("=================")

    # Run the tests
    test_oracle_basics()
    test_angluin_paper_dfa()
