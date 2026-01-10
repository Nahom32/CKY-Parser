from collections import defaultdict
from math import log


class PCFG:
    """
    An Implementation of the probabilistic context free grammar with
    Non-terminals left-handside and terminals right handside. These are
    weighted using probabistic value 0 <= x <= 1. The logistic values are
    stored for ease of computation. It stores the values into three separate
    categories binary, unary and lexical
    """

    def __init__(self):
        self.binary = defaultdict(list)
        self.unary = defaultdict(list)
        self.lexical = defaultdict(list)

    def add_rule(self, lhs, rhs, prob):
        logp = log(prob)
        if len(rhs) == 1 and rhs[0].islower():
            self.lexical[rhs[0]].append((lhs, logp))
        elif len(rhs) == 1:
            self.unary[rhs[0]].append((lhs, logp))
        else:
            self.binary[(rhs[0], rhs[1])].append((lhs, logp))
