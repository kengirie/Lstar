from automata.fa.dfa import DFA
from white_box_oracle import WhiteBoxOracle
from observation_table import ObservationTable
from user_input_oracle import UserInputOracle

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
angluin_paper_dfa = DFA(
    states={"q0", "q1", "q2","q3"},
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
oracle = WhiteBoxOracle(my_dfa)
print(oracle.membership_query(''))
print(oracle.membership_query('101'))
print(oracle.membership_query('100'))
print(oracle.equivalence_query(my_dfa2))
print(oracle.get_num_of_eq())
print(oracle.get_num_of_mq())
observation_table = ObservationTable({'0', '1'})
oracle2 = WhiteBoxOracle(angluin_paper_dfa)
observation_table.fill(oracle2)
print(oracle2.get_num_of_mq())
print(observation_table.to_string())
print(observation_table.make_close())
observation_table.fill(oracle2)
print(observation_table.to_string())
observation_table.build_DFA().show_diagram(path= "first_dfa.png")
cex = str(oracle2.equivalence_query(observation_table.build_DFA()))
print(oracle2.equivalence_query(observation_table.build_DFA()))
print('cex' + cex)
observation_table.counterexample_processing(cex)
observation_table.fill(oracle2)
print(observation_table.to_string())
observation_table.make_consistent()
observation_table.fill(oracle2)
print(observation_table.to_string())
observation_table.build_DFA().show_diagram(path= "second_dfa.png")
cex2 = str(oracle2.equivalence_query(observation_table.build_DFA()))
observation_table.counterexample_processing(cex2)
observation_table.fill(oracle2)
print(observation_table.to_string())
