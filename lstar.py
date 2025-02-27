from observation_table import ObservationTable
from abstract_oracle import AbstractOracle
from automata.fa.dfa import DFA

class LStarAlgorithm:
    """
    Implementation of Angluin's L* algorithm for learning regular languages.
    The algorithm learns a DFA by making membership and equivalence queries to an oracle.
    """

    def __init__(self, input_symbols, oracle: AbstractOracle):
        """
        Initialize the L* algorithm with input symbols and an oracle.

        Args:
            input_symbols: Set of input symbols for the target language
            oracle: An oracle that can answer membership and equivalence queries
        """
        self.input_symbols = input_symbols
        self.oracle = oracle
        self.observation_table = ObservationTable(input_symbols)

    def run(self, max_iterations=100):
        """
        Run the L* algorithm to learn a DFA.

        Args:
            max_iterations: Maximum number of iterations to run the algorithm

        Returns:
            The learned DFA
        """
        # Initialize the observation table
        self.observation_table.fill(self.oracle)

        for i in range(max_iterations):
            print(f"\n--- Iteration {i+1} ---")
            print(self.observation_table.to_string())

            # Make the table closed
            closed_changed = True
            while closed_changed:
                closed_changed = self.observation_table.make_close()
                if closed_changed:
                    self.observation_table.fill(self.oracle)

            # Make the table consistent
            consistent_changed = True
            while consistent_changed:
                consistent_changed = self.observation_table.make_consistent()
                if consistent_changed:
                    self.observation_table.fill(self.oracle)

            # Build a hypothesis DFA
            hypothesis = self.observation_table.build_DFA()
            print("\nCurrent hypothesis DFA:")

            # Ask equivalence query
            result = self.oracle.equivalence_query(hypothesis)

            # If the hypothesis is correct, return it
            if result is True:
                print("\nLearning completed successfully!")
                return hypothesis

            # Otherwise, process the counterexample
            print(f"\nCounterexample received: {result}")
            self.observation_table.counterexample_processing(str(result))
            self.observation_table.fill(self.oracle)

        print("\nMaximum iterations reached without convergence.")
        return self.observation_table.build_DFA()

    def get_statistics(self):
        """
        Get statistics about the learning process.

        Returns:
            Dictionary with statistics
        """
        return {
            "membership_queries": self.oracle.get_num_of_mq(),
            "equivalence_queries": self.oracle.get_num_of_eq()
        }
