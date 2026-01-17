from collections import defaultdict
from math import log
from cky import CKYParser

import re
from visualizer import to_nltk_tree, pretty_print_tree


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

        elif len(rhs) == 2:
            self.binary[(rhs[0], rhs[1])].append((lhs, logp))

        else:
            raise ValueError(f"Non-CNF rule passed to PCFG: {lhs} → {rhs}")


RULE_PATTERN = re.compile(
    r"""
    ^\s*
    (?P<lhs>[A-Za-z_]+)
    \s*→\s*
    (?P<rhs>.+?)
    \s*\[(?P<prob>[0-9.]+)\]
    \s*$
    """,
    re.VERBOSE,
)


def binarize_rule(lhs, rhs, prob):
    """
    Converts A → B C D ... into binary CNF rules.
    """
    if len(rhs) <= 2:
        return [(lhs, rhs, prob)]

    rules = []
    current_lhs = lhs
    remaining_prob = prob

    for i in range(len(rhs) - 2):
        new_nt = f"{lhs}_BIN{i}"
        rules.append((current_lhs, [rhs[i], new_nt], remaining_prob))
        current_lhs = new_nt
        remaining_prob = 1.0

    rules.append((current_lhs, rhs[-2:], 1.0))
    return rules


def normalize_symbol(sym):
    # Remove quotes and normalize terminals
    sym = sym.strip()
    if sym.startswith('"') and sym.endswith('"'):
        return sym[1:-1].lower()
    return sym


def load_pcfg_from_file(path: str) -> PCFG:
    grammar = PCFG()

    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            m = RULE_PATTERN.match(line)
            if not m:
                raise SyntaxError(f"Invalid rule at line {line_no}: {line}")

            lhs = m.group("lhs")
            rhs_raw = m.group("rhs").split()
            rhs = [normalize_symbol(s) for s in rhs_raw]
            prob = float(m.group("prob"))

            cnf_rules = binarize_rule(lhs, rhs, prob)
            for A, B, p in cnf_rules:
                grammar.add_rule(A, B, p)

    return grammar


if __name__ == "__main__":
    pcfg = load_pcfg_from_file("rules.txt")
    parser = CKYParser(pcfg)
    # t = to_nltk_tree(parser.parse("the man saw the dog with the telescope"))
    # t.draw()
    pretty_print_tree(parser.parse("the man saw the dog with the telescope"))
    # print(load_pcfg_from_file("rules.txt"))
