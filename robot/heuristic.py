from resources.consts import Models


def add_by_color(dict, color, value):
    sel_color = "blue"
    if color == "red":
        sel_color = "red"
    dict[sel_color] += value


def x_proximity_value(param):  ### the closer to middle the bigger value
    proximity_map = {0: 1, 1: 2, 2: 3, 3: 4, 4: 4, 5: 3, 6: 2, 7: 1}

    return proximity_map[param]


def get_heuristic(board):
    matrix = board.matrix

    values = {"blue": 0, "red": 0}

    for x in range(8):
        for y in range(8):
            if (x + y) % 2 == 0:
                checker = matrix[x][y]
                if checker is None:
                    continue

                points = 30
                color = "red"
                if checker in Models.KING.value:
                    points += 15

                elif checker in Models.BLUE.value:
                    color = "blue"
                    if y == 7:
                        points += 8
                    points += 7 - y
                else:
                    if y == 0:
                        points += 8
                    points += y
                points += x_proximity_value(x)
                points += len(board.legal_moves((x, y))) * 2
                add_by_color(values, color, points)

    return values["red"] - values["blue"]
