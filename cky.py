from collections import defaultdict


class CKYParser:
    def __init__(self, grammar, k=3, start_symbol="S"):
        self.grammar = grammar
        self.k = k
        self.start = start_symbol

    def parse(self, sentence: str):
        words = sentence.split()
        n = len(words)

        chart = [[defaultdict(list) for _ in range(n + 1)] for _ in range(n)]

        for i, word in enumerate(words):
            if word not in self.grammar.lexical:
                raise ValueError(f"No lexical rule for word: '{word}'")

            for A, logp in self.grammar.lexical[word]:
                tree = (A, word)
                chart[i][i + 1][A].append((logp, tree))

            self._apply_unary_closure(chart, i, i + 1)

        # 2️⃣ CKY dynamic programming
        for span in range(2, n + 1):
            for i in range(n - span + 1):
                j = i + span

                for k in range(i + 1, j):
                    left_cell = chart[i][k]
                    right_cell = chart[k][j]

                    for B in left_cell:
                        for C in right_cell:
                            if (B, C) not in self.grammar.binary:
                                continue

                            for A, rule_logp in self.grammar.binary[(B, C)]:
                                for p1, t1 in left_cell[B]:
                                    for p2, t2 in right_cell[C]:
                                        total_logp = rule_logp + p1 + p2
                                        tree = (A, t1, t2)
                                        chart[i][j][A].append((total_logp, tree))

                self._prune(chart[i][j])
                self._apply_unary_closure(chart, i, j)

        return chart[0][n].get(self.start, [])

    def _prune(self, cell):
        for nt in cell:
            cell[nt] = sorted(cell[nt], key=lambda x: -x[0])[: self.k]

    def _apply_unary_closure(self, chart, i, j):
        """
        Applies A → B rules transitively until convergence.
        """
        updated = True
        while updated:
            updated = False

            for B in list(chart[i][j].keys()):
                if B not in self.grammar.unary:
                    continue

                for A, rule_logp in self.grammar.unary[B]:
                    for p, subtree in chart[i][j][B]:
                        new_p = rule_logp + p
                        new_tree = (A, subtree)

                        if not self._exists(chart[i][j][A], new_tree):
                            chart[i][j][A].append((new_p, new_tree))
                            updated = True

            self._prune(chart[i][j])

    def _exists(self, entries, tree):
        for _, t in entries:
            if t == tree:
                return True
        return False
