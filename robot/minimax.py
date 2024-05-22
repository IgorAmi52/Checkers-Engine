from gui.board import Board
from gui.consts import Models
from robot.heuristic import get_heuristic


def minimax(
    tree,
    is_start=False,
    alpha=float("-inf"),
    beta=float("inf"),
    maximizer=True,
    turn=Models.BLUE.value,
):
    if Board.check_for_endgame(tree.value, turn):  ### check if game is over
        if turn == Models.RED.value:
            tree.heuristic = float("-inf")
            return
        tree.heuristic = float("inf")

    depth = tree.get_tree_depth()

    if depth == 0:  ### last node in tree set heuristic
        tree.set_heuristic(get_heuristic(tree.value))
        return

    if maximizer is True:
        turn = Board.get_next_turn(turn)
        for child in tree.children:
            minimax(child, False, alpha, beta, False, turn)
            set_max_node(tree, child)
            alpha = max(alpha, child.heuristic)
            if beta <= alpha:
                break
        if is_start is True:
            return get_max_node(tree)

    else:
        turn = Board.get_next_turn(turn)
        for child in tree.children:
            minimax(child, False, alpha, beta, True, turn)
            set_min_node(tree, child)
            beta = min(beta, child.heuristic)
            if alpha <= beta:
                break


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
