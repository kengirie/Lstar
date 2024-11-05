from automata.fa.dfa import DFA
from white_box_oracle import WhiteBoxOracle

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
oracle = WhiteBoxOracle(my_dfa)
print(oracle.membership_query(''))
print(oracle.membership_query('101'))
print(oracle.membership_query('100'))
print(oracle.equivalence_query(my_dfa2))
print(oracle.get_num_of_eq())
print(oracle.get_num_of_mq())
