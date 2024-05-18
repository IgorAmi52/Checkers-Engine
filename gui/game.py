import pygame
import sys


from gui.board import Board
from gui.graphics import Graphics
from gui.consts import Colors
from robot.heuristic import get_heuristic

pygame.font.init()


class Game:
    """
    The main game control.
    """

    def __init__(self):
        self.graphics = Graphics()
        self.board = Board()

        self.turn = Colors.BLUE.value
        self.selected_piece = None  # a board location.
        self.hop = False
        self.selected_legal_moves = []

    def main(self):
        """ "This executes the game and controls its flow."""
        self.setup()

        while True:  # main game loop
            self.event_loop()
            self.update()

    def setup(self):
        """Draws the window and board at the beginning of the game"""
        self.graphics.setup_window()

    def event_loop(self):
        """
        The event loop. This is where events are triggered
        (like a mouse click) and then effect the game state.
        """

        self.mouse_pos = self.graphics.board_coords(
            pygame.mouse.get_pos()
        )  # what square is the mouse in?
        if self.selected_piece is not None:
            self.selected_legal_moves = self.board.legal_moves(
                self.selected_piece, self.hop
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminate_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hop is False:
                    if (
                        self.board.location(self.mouse_pos).occupant is not None
                        and self.board.location(self.mouse_pos).occupant.color
                        == self.turn
                    ):  # picked your checker
                        self.selected_piece = self.mouse_pos

                    elif (
                        self.selected_piece is not None
                        and self.mouse_pos
                        in self.board.legal_moves(self.selected_piece)
                    ):  # moved checker
                        self.board.move_piece(self.selected_piece, self.mouse_pos)

                        if self.mouse_pos not in self.board.adjacent(
                            self.selected_piece
                        ):
                            self.board.remove_piece(
                                (
                                    (self.selected_piece[0] + self.mouse_pos[0]) >> 1,
                                    (self.selected_piece[1] + self.mouse_pos[1]) >> 1,
                                )
                            )

                            self.hop = True
                            self.selected_piece = self.mouse_pos

                        else:
                            self.end_turn()

                if self.hop is True:
                    if (
                        self.selected_piece is not None
                        and self.mouse_pos
                        in self.board.legal_moves(self.selected_piece, self.hop)
                    ):
                        self.board.move_piece(self.selected_piece, self.mouse_pos)
                        self.board.remove_piece(
                            (
                                (self.selected_piece[0] + self.mouse_pos[0]) >> 1,
                                (self.selected_piece[1] + self.mouse_pos[1]) >> 1,
                            )
                        )

                    if self.board.legal_moves(self.mouse_pos, self.hop) == []:
                        self.end_turn()

                    else:
                        self.selected_piece = self.mouse_pos
                print(get_heuristic(self.board))

    def update(self):
        """Calls on the graphics class to update the game display."""
        self.graphics.update_display(
            self.board, self.selected_legal_moves, self.selected_piece
        )

    def terminate_game(self):
        """Quits the program and ends the game."""
        pygame.quit()
        sys.exit

    def end_turn(self):
        """
        End the turn. Switches the current player.
        end_turn() also checks for and game and resets a lot of class attributes.
        """
        if self.turn == Colors.BLUE.value:
            self.turn = Colors.RED.value
        else:
            self.turn = Colors.BLUE.value

        self.selected_piece = None
        self.selected_legal_moves = []
        self.hop = False

        if self.check_for_endgame():
            if self.turn == Colors.BLUE.value:
                self.graphics.draw_message("RED WINS!")
            else:
                self.graphics.draw_message("BLUE WINS!")

    def check_for_endgame(self):
        """
        Checks to see if a player has run out of moves or pieces. If so, then return True. Else return False.
        """
        for x in range(8):
            for y in range(8):
                if (
                    self.board.location((x, y)).color == Colors.BLACK.value
                    and self.board.location((x, y)).occupant is not None
                    and self.board.location((x, y)).occupant.color == self.turn
                ):
                    if self.board.legal_moves((x, y)) != []:
                        return False

        return True