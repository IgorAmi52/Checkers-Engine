from gui.consts import Colors


def get_heuristic(board):
    matrix = board.matrix

    values = {"blue": 0, "red": 0}

    for x in range(8):
        for y in range(8):
            if (x + y) % 2 == 0:
                checker = matrix[x][y].occupant
                if checker is None:
                    continue
                color = checker.color
                isKing = checker.king

                if x != 0 and x != 7:
                    add_by_color(values, color, 1)
                if isKing is True:
                    add_by_color(values, color, 10)
                    continue
                if color == Colors.BLUE.value:
                    add_by_color(values, color, 7 - y)
                else:
                    add_by_color(values, color, y)

    return values["red"] - values["blue"]


def add_by_color(dict, color, value):
    sel_color = "blue"
    if color == Colors.RED.value:
        sel_color = "red"
    dict[sel_color] += value
