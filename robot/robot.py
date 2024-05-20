import copy
from gui.consts import Colors, Models
from robot.minimax import minimax
from robot.tree_node import TreeNode
import logging
import time


class Robot:
    def move(self, board):
        first = time.time()
        tree = self.set_tree(TreeNode(board), 3)
        logging.info("Time: " + str(time.time() - first))

        best_node = minimax(tree, True)
        return best_node.value

    def set_tree(self, tree, depth):
        if depth == 0:
            tree = None
            return

        tree.children = []
        board = tree.value
        matrix = board.matrix

        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 0:
                    checker = matrix[x][y]
                    if checker is None:
                        continue
                    if checker not in Models.RED.value:
                        continue
                    ### selected a red checker

                    self.create_children(tree, tree.value, (x, y))

                    for child in tree.children:
                        self.set_tree(child, depth - 1)
        return tree

    def create_children(self, tree, board, curr_pos, hop=False):
        for move in board.legal_moves(curr_pos, hop):
            new_board = copy.deepcopy(board)
            new_board.move_piece(curr_pos, move)
            if move not in new_board.adjacent(curr_pos):
                new_board.remove_piece(
                    (
                        (curr_pos[0] + move[0]) >> 1,
                        (curr_pos[1] + move[1]) >> 1,
                    )
                )
                if len(new_board.legal_moves(move, True)) != 0:  ### hop has more move
                    self.create_children(tree, new_board, move, True)
                    return
            node = TreeNode(new_board)
            tree.children.append(node)
