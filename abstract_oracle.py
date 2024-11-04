from abc import ABC, abstractmethod


class AbstractOracle(ABC):
    def __init__(self,target):
        self.target = target
        self.num_of_eq = 0
        self.num_of_mq = 0

    @abstractmethod
    def equivalence_query_impl(self, hypothesis):
        pass

    @abstractmethod
    def membership_query_impl(self, word):
        pass

    def equivalence_query(self, hypothesis):
        self.num_of_eq += 1
        return self.equivalence_query_impl(hypothesis)

    def membership_query(self, word):
        self.num_of_mq += 1
        return self.membership_query_impl(word)

    def get_num_of_eq(self):
        return self.num_of_eq

    def get_num_of_mq(self):
        return self.num_of_mq
