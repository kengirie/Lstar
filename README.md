# L* Algorithm Implementation

This project implements Dana Angluin's L* algorithm for learning regular languages, as described in her 1987 paper "Learning Regular Sets from Queries and Counterexamples".

## Overview

The L* algorithm is a query-based learning algorithm that learns a deterministic finite automaton (DFA) by making two types of queries to a teacher (oracle):

1. **Membership queries**: "Is string w in the target language?"
2. **Equivalence queries**: "Is my hypothesis DFA equivalent to the target DFA?"

The algorithm builds an observation table to organize information about the language and iteratively refines a hypothesis DFA until it correctly represents the target language.

## Files

- `abstract_oracle.py`: Abstract base class for oracles
- `white_box_oracle.py`: Oracle implementation for testing with known DFAs
- `user_input_oracle.py`: Oracle implementation that uses user input
- `observation_table.py`: Implementation of the observation table data structure
- `lstar.py`: Main implementation of the L* algorithm
- `test.py`: Basic tests for the oracles and L* algorithm
- `lstar_test.py`: More comprehensive test suite for the L* algorithm

## Usage

### Running the Basic Tests

```bash
python test.py
```

This will run basic tests for the oracle functionality and test the L* algorithm with the DFA from Angluin's paper.

### Running the Test Suite

```bash
python lstar_test.py
```

This will present a menu with several test options:

1. Test with a simple DFA (that accepts strings with an odd number of 1s)
2. Test with Angluin's paper DFA
3. Test with user input (you define your own language)
4. Exit

### Using the L* Algorithm in Your Own Code

```python
from automata.fa.dfa import DFA
from white_box_oracle import WhiteBoxOracle
from lstar import LStarAlgorithm

# Define a target DFA
target_dfa = DFA(
    states={'q0', 'q1'},
    input_symbols={'0', '1'},
    transitions={
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q1', '1': 'q0'}
    },
    initial_state='q0',
    final_states={'q1'}
)

# Create an oracle for the target DFA
oracle = WhiteBoxOracle(target_dfa)

# Create and run the L* algorithm
lstar = LStarAlgorithm({'0', '1'}, oracle)
learned_dfa = lstar.run()

# Print statistics
stats = lstar.get_statistics()
print(f"Learning completed with:")
print(f"- {stats['membership_queries']} membership queries")
print(f"- {stats['equivalence_queries']} equivalence queries")

# Visualize the learned DFA
learned_dfa.show_diagram(path="learned_dfa.png")
```

## Algorithm Details

The L* algorithm works as follows:

1. Initialize an observation table with S = E = {ε} (empty string)
2. Fill the table with membership query results
3. Repeat until the hypothesis is correct:
   a. Make the table closed and consistent
   b. Build a hypothesis DFA from the table
   c. Make an equivalence query
   d. If the hypothesis is correct, return it
   e. Otherwise, process the counterexample and update the table

### Observation Table

The observation table consists of:
- S: A set of prefixes (representing states)
- E: A set of suffixes (experiments to distinguish states)
- f: A function mapping (s, e) pairs to boolean values (membership query results)

A table is:
- **Closed** if for each r ∈ S·Σ, there exists s ∈ S such that row(r) = row(s)
- **Consistent** if for all s1, s2 ∈ S where row(s1) = row(s2), for all a ∈ Σ, row(s1·a) = row(s2·a)

## Dependencies

- [automata-lib](https://pypi.org/project/automata-lib/): For DFA implementation and visualization
- [overrides](https://pypi.org/project/overrides/): For method overriding annotations

## References

- Angluin, D. (1987). Learning regular sets from queries and counterexamples. Information and Computation, 75(2), 87-106.
