from gui.consts import Colors, Directions
from gui.square import Square
from gui.piece import Piece


class Board:
    def __init__(self):
        self.matrix = self.new_board()

    def new_board(self):
        """
        Create a new board matrix.
        """

        # initialize squares and place them in matrix

        matrix = [[None] * 8 for i in range(8)]

        for x in range(8):
            for y in range(8):
                if (x + y) % 2 != 0:
                    matrix[x][y] = Square(Colors.WHITE.value)
                else:
                    matrix[x][y] = Square(Colors.BLACK.value)

        # initialize the pieces and put them in the appropriate squares

        for x in range(8):
            for y in range(3):
                if matrix[x][y].color == Colors.BLACK.value:
                    matrix[x][y].occupant = Piece(Colors.RED.value)
            for y in range(5, 8):
                if matrix[x][y].color == Colors.BLACK.value:
                    matrix[x][y].occupant = Piece(Colors.BLUE.value)

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
        if self.matrix[x][y].occupant is not None:
            if (
                self.matrix[x][y].occupant.king is False
                and self.matrix[x][y].occupant.color is Colors.BLUE.value
            ):
                blind_legal_moves = [
                    self.rel(Directions.NORTHWEST.value, (x, y)),
                    self.rel(Directions.NORTHEAST.value, (x, y)),
                ]

            elif (
                self.matrix[x][y].occupant.king is False
                and self.matrix[x][y].occupant.color is Colors.RED.value
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
                    if self.location(move).occupant is None:
                        legal_moves.append(move)
                    elif (
                        self.location(move).occupant.color
                        is not self.location((x, y)).occupant.color
                        and self.on_board(
                            (move[0] + (move[0] - x), move[1] + (move[1] - y))
                        )
                        and self.location(
                            (move[0] + (move[0] - x), move[1] + (move[1] - y))
                        ).occupant
                        is None
                    ):  # is this location filled by an enemy piece?
                        legal_moves.append(
                            (move[0] + (move[0] - x), move[1] + (move[1] - y))
                        )

        else:  # hop == True
            for move in blind_legal_moves:
                if self.on_board(move) and self.location(move).occupant is not None:
                    if (
                        self.location(move).occupant.color
                        != self.location((x, y)).occupant.color
                        and self.on_board(
                            (move[0] + (move[0] - x), move[1] + (move[1] - y))
                        )
                        and self.location(
                            (move[0] + (move[0] - x), move[1] + (move[1] - y))
                        ).occupant
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
        self.matrix[x][y].occupant = None

    def move_piece(self, pixel_start, pixel_end):
        """
        Move a piece from (start_x, start_y) to (end_x, end_y).
        """
        start_x = pixel_start[0]
        start_y = pixel_start[1]
        end_x = pixel_end[0]
        end_y = pixel_end[1]

        self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
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
        if self.location((x, y)).occupant is not None:
            if (
                self.location((x, y)).occupant.color == Colors.BLUE.value and y == 0
            ) or (self.location((x, y)).occupant.color == Colors.RED.value and y == 7):
                self.location((x, y)).occupant.king = True
