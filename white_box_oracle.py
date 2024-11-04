from automata.fa.dfa import DFA
class WhiteBoxOracle:
    def __init__(self, target):
        self.target = target
        self.num_of_eq = 0
        self.num_of_mq = 0

    def equivalence_query(self, hypothesis):
        self.num_of_eq += 1
        sym_diff = self.target.symmetric_difference(hypothesis)
        if (sym_diff.isempty()):
            return True
        else :
            return sym_diff.minimum_word_length()
    def membership_query(self, word):
        self.num_of_mq += 1
        return self.target.accepts_input(word)

    def get_num_of_eq(self):
        return self.num_of_eq

    def get_num_of_mq(self):
        return self.num_of_mq
