from nltk import Tree


def pretty_print_tree(tree, indent=0):
    """
    Recursively prints a parse tree in bracketed form.
    """
    space = "  " * indent

    if isinstance(tree, tuple) and len(tree) == 2 and isinstance(tree[1], str):
        print(f"{space}({tree[0]} {tree[1]})")
        return

    if len(tree) == 2:
        print(f"{space}({tree[0]}")
        pretty_print_tree(tree[1], indent + 1)
        print(f"{space})")
        return

    label, left, right = tree
    print(f"{space}({label}")
    pretty_print_tree(left, indent + 1)
    pretty_print_tree(right, indent + 1)
    print(f"{space})")


def to_nltk_tree(tree):
    if len(tree) == 2 and isinstance(tree[1], str):
        return Tree(tree[0], [tree[1]])

    if len(tree) == 2:
        return Tree(tree[0], [to_nltk_tree(tree[1])])

    label, left, right = tree
    return Tree(label, [to_nltk_tree(left), to_nltk_tree(right)])
