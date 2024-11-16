from automata.fa.dfa import DFA
from abstract_oracle import AbstractOracle
from overrides import overrides

class WhiteBoxOracle(AbstractOracle):

    @overrides
    def equivalence_query_impl(self, hypothesis):
        sym_diff = self.target.symmetric_difference(hypothesis)
        if (sym_diff.isempty()):
            return True
        else :
            return sym_diff.random_word(sym_diff.minimum_word_length())

    @overrides
    def membership_query_impl(self, word):
        return self.target.accepts_input(word)
