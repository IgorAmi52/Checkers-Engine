from robot.heuristic import get_heuristic


def minimax(
    tree,
    is_start=False,
    alpha=float("-inf"),
    beta=float("inf"),
    maximizer=True,
):
    depth = tree.get_tree_depth()

    if depth == 0:  ### last node in tree set heuristic
        tree.set_heuristic(get_heuristic(tree.value))
        return

    if maximizer is True:
        for child in tree.children:
            if child.heuristic is None:
                minimax(child, False, alpha, beta, False)
            set_max_node(tree, child)
            # alpha = max(alpha, child.heuristic)
            # if beta <= alpha:
            #     print("gas")
            #     break
        if is_start is True:
            return get_max_node(tree)

    else:
        for child in tree.children:
            if child.heuristic is None:
                minimax(child, False, alpha, beta, True)
            set_min_node(tree, child)
            # beta = min(beta, child.heuristic)
            # if alpha <= beta:
            #     print("gas")
            #     break


def get_max_node(tree):
    max = tree.children[0]
    for child in tree.children:
        if max.heuristic < child.heuristic:
            max = child
    return max


def set_max_node(tree, child):
    if tree.heuristic is None:
        tree.heuristic = child.heuristic
    elif tree.heuristic < child.heuristic:
        tree.heuristic = child.heuristic


def set_min_node(tree, child):
    if tree.heuristic is None:
        tree.heuristic = child.heuristic
    elif tree.heuristic > child.heuristic:
        tree.heuristic = child.heuristic
