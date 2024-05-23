import pygame
import sys


from gui.board import Board
from gui.graphics import Graphics
from resources.consts import Models
from robot.robot import Robot

pygame.font.init()


class Game:
    """
    The main game control.
    """

    def __init__(self):
        self.graphics = Graphics()
        self.board = Board()
        self.robot = Robot()
        self.turn = Models.BLUE.value
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

        if self.turn == Models.RED.value and not Board.check_for_endgame(
            self.board, self.turn
        ):  ### robots turn
            self.board = self.robot.move(self.board)
            self.end_turn()
            return

        self.mouse_pos = self.graphics.board_coords(  ### [x,y] of the matrix
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
                    if (  ### click on the checker to move
                        self.board.location(self.mouse_pos) is not None
                        and self.board.location(self.mouse_pos) in self.turn
                    ):
                        self.selected_piece = self.mouse_pos

                    elif (  ### click on the place you want to move
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
        if self.turn == Models.BLUE.value:
            self.turn = Models.RED.value
        else:
            self.turn = Models.BLUE.value

        self.selected_piece = None
        self.selected_legal_moves = []
        self.hop = False
        if Board.check_for_endgame(self.board, self.turn):
            if self.turn == Models.BLUE.value:
                self.graphics.draw_message("RED WINS!")
            else:
                self.graphics.draw_message("BLUE WINS!")
