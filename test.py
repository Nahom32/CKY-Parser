from pcfg import PCFG, load_pcfg_from_file
from cky import CKYParser
from visualizer import pretty_print_tree

test_sentences = [
    "the man saw the dog",
    "the dog chased the cat",
    "the man saw the dog with the telescope",
    "the dog saw the man in the park",
    "the big dog saw the small cat",
    "the man and the woman saw the dog",
    "the man quickly saw the dog",
    "the woman saw the man with the telescope",
    "the dog walked in the park",
    "the man liked the dog",
]


results = {}
grammar = load_pcfg_from_file("rules.txt")
# pcfg = PCFG(grammar)
parser = CKYParser(grammar)
for sent in test_sentences:
    parses = parser.parse(sent)
    results[sent] = parses

    print(f"\nSentence: {sent}")
    print(f"Number of parses: {len(parses)}")

    if parses:
        logp, tree = parses[0]
        pretty_print_tree(tree)
