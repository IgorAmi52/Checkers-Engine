##COLORS##
from enum import Enum


class Colors(Enum):
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    GOLD = (255, 215, 0)
    HIGH = (160, 190, 255)


class Models(Enum):
    BLUE = [-1, -2]
    RED = [1, 2]
    KING = [-2, 2]


class Directions(Enum):
    NORTHWEST = "northwest"
    NORTHEAST = "northeast"
    SOUTHWEST = "southwest"
    SOUTHEAST = "southeast"
