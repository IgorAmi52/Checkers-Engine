from robot.heuristic import get_heuristic


def minimax(
    tree, is_start=False, alpha=float("-inf"), beta=float("inf"), maximizer=True
):
    if not tree.children:  # If the node is a leaf node
        tree.set_heuristic(get_heuristic(tree.value))
        return

    if maximizer:
        max_heuristic = float("-inf")
        best_child = None
        for child in tree.children:
            if child.heuristic is None:
                minimax(child, False, alpha, beta, False)
            if child.heuristic > max_heuristic:
                max_heuristic = child.heuristic
                best_child = child
            alpha = max(alpha, max_heuristic)
            if beta <= alpha:
                break  # Beta cut-off
        tree.heuristic = max_heuristic
        if is_start:
            return best_child
    else:
        min_heuristic = float("inf")
        for child in tree.children:
            if child.heuristic is None:
                minimax(child, False, alpha, beta, True)
            if child.heuristic < min_heuristic:
                min_heuristic = child.heuristic
            beta = min(beta, min_heuristic)
            if beta <= alpha:
                break  # Alpha cut-off
        tree.heuristic = min_heuristic


# Function to get the child with the highest heuristic value
def get_max_node(tree):
    max_child = tree.children[0]
    for child in tree.children:
        if child.heuristic > max_child.heuristic:
            max_child = child
    return max_child
