import copy
from gui.consts import Colors
from robot.minimax import minimax
from robot.tree_node import TreeNode


class Robot:
    def move(self, board):
        tree = self.set_tree(TreeNode(board), 2)
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
                    checker = matrix[x][y].occupant
                    if checker is None:
                        continue
                    if checker.color != Colors.RED.value:
                        continue
                    ### selected a red checker

                    for move in board.legal_moves((x, y)):
                        new_board = copy.deepcopy(board)
                        self.move_peace(new_board, (x, y), move)
                        node = TreeNode(new_board)
                        tree.children.append(node)

                    for child in tree.children:
                        self.set_tree(child, depth - 1)
        return tree

    def move_peace(self, board, curr_pos, mov_pos):
        board.move_piece(curr_pos, mov_pos)

        if mov_pos not in board.adjacent(curr_pos):
            board.remove_piece(
                (
                    (curr_pos[0] + mov_pos[0]) >> 1,
                    (curr_pos[1] + mov_pos[1]) >> 1,
                )
            )
