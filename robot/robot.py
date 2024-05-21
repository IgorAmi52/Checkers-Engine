import copy
from gui.consts import Models
from robot.minimax import minimax
from robot.tree_node import TreeNode


class Robot:
    tree = None

    def move(self, board):
        depth = 0
        if self.tree is None:
            self.tree = TreeNode(board)
            depth = 3
        else:
            self.tree = self.find_matching_board(self.tree.children, board)
            depth = 2

        self.set_tree(self.tree, Models.RED.value, depth)

        self.tree = minimax(self.tree, True)

        return self.tree.value

    def set_tree(self, tree, turn, depth):
        if tree is not None and tree.get_tree_depth() != 0:
            turn = self.get_next_turn(turn)
            for child in tree.children:
                self.set_tree(child, turn, depth)
            return

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
                    if checker not in turn:
                        continue
                    self.create_children(tree, tree.value, (x, y))
        # for child in tree.children:
        #     print_matrix(child.value.matrix)
        #     print("\n")

        turn = self.get_next_turn(turn)
        for child in tree.children:
            self.set_tree(child, turn, depth - 1)

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
            node = TreeNode(new_board)
            tree.children.append(node)

    def find_matching_board(self, arr, board):
        for item in arr:
            if self.are_matrices_identical(item.value.matrix, board.matrix) is True:
                return item
        return None

    def are_matrices_identical(self, matrix1, matrix2):
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            return False
        for i in range(len(matrix1)):
            for j in range(len(matrix1[0])):
                if matrix1[i][j] != matrix2[i][j]:
                    return False
        return True

    def get_next_turn(self, turn):
        if turn == Models.RED.value:
            return Models.BLUE.value
        return Models.RED.value


def print_matrix(matrix):
    for i in range(8):
        row = ""
        for y in range(8):
            row += str(matrix[y][i]) + " "

        print(row)
