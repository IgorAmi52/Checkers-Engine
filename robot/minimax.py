from robot.heuristic import get_heuristic


def minimax(
    tree, is_start=False, alpha=float("-inf"), beta=float("inf"), maximizer=True
):
    if not tree.children:  # If the node is a leaf node
        tree.set_heuristic(get_heuristic(tree.value))
        return tree.heuristic

    if maximizer:
        max_heuristic = float("-inf")
        best_child = None
        for child in tree.children:
            if child.heuristic is not None:
                child_heuristic = child.heuristic
            else:
                child_heuristic = minimax(child, False, alpha, beta, False)
            if child_heuristic > max_heuristic:
                max_heuristic = child_heuristic
                best_child = child
            alpha = max(alpha, max_heuristic)
            if beta <= alpha:
                break  # Beta cut-off
        tree.heuristic = max_heuristic
        if is_start:
            tree.visualize_tree()
            return best_child
        return max_heuristic
    else:
        min_heuristic = float("inf")
        for child in tree.children:
            if child.heuristic is not None:
                child_heuristic = child.heuristic
            else:
                child_heuristic = minimax(child, False, alpha, beta, True)
            min_heuristic = min(min_heuristic, child_heuristic)
            beta = min(beta, min_heuristic)
            if beta <= alpha:
                break  # Alpha cut-off
        tree.heuristic = min_heuristic
        return min_heuristic


# Usage:
# Assuming `tree` is your root node and `get_heuristic` is correctly defined
