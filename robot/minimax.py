from robot.heuristic import get_heuristic
from robot.tree_node import TreeNode


def minimax(tree, is_start=False, maximizer=True):
    depth = tree.get_tree_depth()

    if depth == 0:
        return

    if depth == 1:
        for child in tree.children:
            child.set_heuristic(get_heuristic(child.value))

    if maximizer is True:
        for child in tree.children:
            minimax(child, False, False)
        if is_start is True:
            return max_node(tree)
        max_node(tree)

    else:
        for child in tree.children:
            minimax(child, False, True)
        min_node(tree)


def max_node(node):
    max_node_heuristic = node.children[0].heuristic
    max_node = node.children[0]
    for child in node.children:
        if child.heuristic > max_node_heuristic:
            max_node_heuristic = child.heuristic
            max_node = child
    node.set_heuristic(max_node_heuristic)
    return max_node


def min_node(node):
    min_node_heuristic = node.children[0].heuristic
    for child in node.children:
        if child.heuristic < min_node_heuristic:
            min_node_heuristic = child.heuristic
    node.set_heuristic(min_node_heuristic)
