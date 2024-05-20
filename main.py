import logging

from gui.game import Game


def main():
    game = Game()
    game.main()


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    filemode="w",
    format="%(levelname)s - %(message)s",
)

if __name__ == "__main__":
    main()

    """in board merge method blind_legal_moves with legal_moves
    highlight doesn't work sometimes
    change consts to enum
    """
