from collections import defaultdict


class CKYParser:
    def __init__(self, grammar, k=3):
        self.grammar = grammar
        self.k = k

    def parse(self, sentence):
        words = sentence.split()
        n = len(words)
        chart = [[defaultdict(list) for _ in range(n + 1)] for _ in range(n)]

        # Initialization (lexical rules)
        for i, word in enumerate(words):
            for lhs, logp in self.grammar.lexical[word]:
                chart[i][i + 1][lhs].append((logp, word))
            self._unary_closure(chart, i, i + 1)

        # CKY dynamic programming
        for span in range(2, n + 1):
            for i in range(n - span + 1):
                j = i + span
                for k in range(i + 1, j):
                    for B in chart[i][k]:
                        for C in chart[k][j]:
                            for A, logp in self.grammar.binary.get((B, C), []):
                                for p1, bp1 in chart[i][k][B]:
                                    for p2, bp2 in chart[k][j][C]:
                                        chart[i][j][A].append(
                                            (logp + p1 + p2, (A, bp1, bp2))
                                        )
                self._prune(chart[i][j])
                self._unary_closure(chart, i, j)

        return chart[0][n].get("S", [])

    def _prune(self, cell):
        for nt in cell:
            cell[nt] = sorted(cell[nt], reverse=True)[: self.k]

    def _unary_closure(self, chart, i, j):
        added = True
        while added:
            added = False
            for B in list(chart[i][j]):
                for A, logp in self.grammar.unary.get(B, []):
                    for p, bp in chart[i][j][B]:
                        entry = (p + logp, bp)
                        if entry not in chart[i][j][A]:
                            chart[i][j][A].append(entry)
                            added = True
            self._prune(chart[i][j])
