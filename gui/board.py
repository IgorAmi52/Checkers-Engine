from resources.consts import Directions, Models


class Board:
    def __init__(self):
        self.matrix = self.new_board()

    def new_board(self):
        """
        Create a new board matrix.
        """

        # initialize squares and place them in matrix

        matrix = [[None] * 8 for i in range(8)]

        # initialize the pieces and put them in the appropriate squares

        for x in range(8):
            for y in range(3):
                if (x + y) % 2 == 0:
                    matrix[x][y] = 1
            for y in range(5, 8):
                if (x + y) % 2 == 0:
                    matrix[x][y] = -1

        return matrix

    def rel(self, dir, pixel):
        """
                Returns the coordinates one square in a different direction to (x,y).
        )
        """
        x = pixel[0]
        y = pixel[1]
        if dir == Directions.NORTHWEST.value:
            return (x - 1, y - 1)
        elif dir == Directions.NORTHEAST.value:
            return (x + 1, y - 1)
        elif dir == Directions.SOUTHWEST.value:
            return (x - 1, y + 1)
        elif dir == Directions.SOUTHEAST.value:
            return (x + 1, y + 1)
        else:
            return 0

    def adjacent(self, pixel):
        """
        Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
        """
        x = pixel[0]
        y = pixel[1]

        return [
            self.rel(Directions.NORTHWEST.value, (x, y)),
            self.rel(Directions.NORTHEAST.value, (x, y)),
            self.rel(Directions.SOUTHWEST.value, (x, y)),
            self.rel(Directions.SOUTHEAST.value, (x, y)),
        ]

    def location(self, pixel):
        """
        Takes a set of coordinates as arguments and returns self.matrix[x][y]
        This can be faster than writing something like self.matrix[coords[0]][coords[1]]
        """
        x = pixel[0]
        y = pixel[1]

        return self.matrix[x][y]

    def blind_legal_moves(self, pixel):
        """
        Returns a list of blind legal move locations from a set of coordinates (x,y) on the board.
        If that location is empty, then blind_legal_moves() return an empty list.
        """

        x = pixel[0]
        y = pixel[1]
        if self.matrix[x][y] is not None:
            if (
                self.matrix[x][y] not in Models.KING.value
                and self.matrix[x][y] in Models.BLUE.value
            ):
                blind_legal_moves = [
                    self.rel(Directions.NORTHWEST.value, (x, y)),
                    self.rel(Directions.NORTHEAST.value, (x, y)),
                ]

            elif (
                self.matrix[x][y] not in Models.KING.value
                and self.matrix[x][y] in Models.RED.value
            ):
                blind_legal_moves = [
                    self.rel(Directions.SOUTHWEST.value, (x, y)),
                    self.rel(Directions.SOUTHEAST.value, (x, y)),
                ]

            else:
                blind_legal_moves = [
                    self.rel(Directions.NORTHWEST.value, (x, y)),
                    self.rel(Directions.NORTHEAST.value, (x, y)),
                    self.rel(Directions.SOUTHWEST.value, (x, y)),
                    self.rel(Directions.SOUTHEAST.value, (x, y)),
                ]

        else:
            blind_legal_moves = []

        return blind_legal_moves

    def legal_moves(self, pixel, hop=False):
        """
        Returns a list of legal move locations from a given set of coordinates (x,y) on the board.
        If that location is empty, then legal_moves() returns an empty list.
        """

        x = pixel[0]
        y = pixel[1]
        blind_legal_moves = self.blind_legal_moves((x, y))
        legal_moves = []

        if hop is False:
            for move in blind_legal_moves:
                if self.on_board(move):
                    if self.location(move) is None:
                        legal_moves.append(move)
                    elif (
                        self.location(move) * self.location((x, y))
                        < 0  ### are they not the same color
                        and self.on_board(
                            (move[0] + (move[0] - x), move[1] + (move[1] - y))
                        )
                        and self.location(
                            (move[0] + (move[0] - x), move[1] + (move[1] - y))
                        )
                        is None
                    ):  # is this location filled by an enemy piece?
                        legal_moves.append(
                            (move[0] + (move[0] - x), move[1] + (move[1] - y))
                        )

        else:  # hop == True
            for move in blind_legal_moves:
                if self.on_board(move) and self.location(move) is not None:
                    if (
                        self.location(move) * self.location((x, y))
                        < 0  ### are they not the same color
                        and self.on_board(
                            (move[0] + (move[0] - x), move[1] + (move[1] - y))
                        )
                        and self.location(
                            (move[0] + (move[0] - x), move[1] + (move[1] - y))
                        )
                        is None
                    ):  # is this location filled by an enemy piece?
                        legal_moves.append(
                            (move[0] + (move[0] - x), move[1] + (move[1] - y))
                        )

        return legal_moves

    def remove_piece(self, pixel):
        """
        Removes a piece from the board at position (x,y).
        """
        x = pixel[0]
        y = pixel[1]
        self.matrix[x][y] = None

    def move_piece(self, pixel_start, pixel_end):
        """
        Move a piece from (start_x, start_y) to (end_x, end_y).
        """
        start_x = pixel_start[0]
        start_y = pixel_start[1]
        end_x = pixel_end[0]
        end_y = pixel_end[1]

        self.matrix[end_x][end_y] = self.matrix[start_x][start_y]
        self.remove_piece((start_x, start_y))

        self.king((end_x, end_y))

    def is_end_square(self, coords):
        """
        Is passed a coordinate tuple (x,y), and returns true or
        false depending on if that square on the board is an end square.

        ===DOCTESTS===

        >>> board = Board()

        >>> board.is_end_square((2,7))
        True

        >>> board.is_end_square((5,0))
        True

        >>>board.is_end_square((0,5))
        False
        """

        if coords[1] == 0 or coords[1] == 7:
            return True
        else:
            return False

    def on_board(self, pixel):
        """
        Checks to see if the given square (x,y) lies on the board.
        If it does, then on_board() return True. Otherwise it returns false.

        ===DOCTESTS===
        >>> board = Board()

        >>> board.on_board((5,0)):
        True

        >>> board.on_board(-2, 0):
        False

        >>> board.on_board(3, 9):
        False
        """

        x = pixel[0]
        y = pixel[1]
        if x < 0 or y < 0 or x > 7 or y > 7:
            return False
        else:
            return True

    def king(self, pixel):
        """
        Takes in (x,y), the coordinates of square to be considered for kinging.
        If it meets the criteria, then king() kings the piece in that square and kings it.
        """
        x = pixel[0]
        y = pixel[1]
        if self.location((x, y)) is not None:
            if self.location((x, y)) == -1 and y == 0:  ### if blue change to king red
                self.matrix[x][y] = -2
            elif self.location((x, y)) == 1 and y == 7:  ### if red change to king blue
                self.matrix[x][y] = 2

    def find_matching_board(arr, board):
        for item in arr:
            if Board.are_matrices_identical(item.value.matrix, board.matrix) is True:
                return item
        return None

    def are_matrices_identical(matrix1, matrix2):
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            return False
        for i in range(len(matrix1)):
            for j in range(len(matrix1[0])):
                if matrix1[i][j] != matrix2[i][j]:
                    return False
        return True

    def check_for_endgame(board, turn):
        """
        Checks to see if a player has run out of moves or pieces. If so, then return True. Else return False.
        """
        for x in range(8):
            for y in range(8):
                if (
                    (x + y) % 2 == 0
                    and board.location((x, y)) is not None
                    and board.location((x, y)) in turn
                ):
                    if board.legal_moves((x, y)) != []:
                        return False

        return True

    def get_next_turn(turn):
        if turn == Models.RED.value:
            return Models.BLUE.value
        return Models.RED.value

    def get_piece_count(board):
        matrix = board.matrix
        count = 0

        for x in range(8):
            for y in range(8):
                if matrix[x][y] is not None:
                    count += 1
        return count
