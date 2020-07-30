# ------------------------------------------------------
import re
from copy import deepcopy
from pyswip import Prolog
# ------------------------------------------------------
# ------------------------------------------------------

class Direction:
    TURN_CLOCKWISE = 'c'
    TURN_COUNTER_CLOCKWISE = 'cc'
# ------------------------------------------------------

# ------------------------------------------------------
class Color:
    WHITE = 'w'
    YELLOW = 'y'
    RED = 'r'
    BLUE = 'b'
    ORANGE = 'o'
    GREEN = 'g'
# ------------------------------------------------------

# ------------------------------------------------------
class Cell:
    def __init__(self, colors={}):
        self.clear()
        self.set_colors(colors)

    def clear(self):
        self.colors = {
            Face.TOP: None,
            Face.LEFT: None,
            Face.FRONT: None,
            Face.RIGHT: None,
            Face.BACK: None,
            Face.BOTTOM: None,
        }

    def clone(self):
        return Cell(self.colors)

    def copy_from(self, cell):
        self.clear()
        self.set_colors(cell.colors)
        return self

    def set_colors(self, colors):
        for face in colors:
            self.set_color(face, colors[face])

    def set_color(self, face, color):
        if face in self.colors:
            self.colors[face] = color

    def get_color(self, face):
        return self.colors[face] if face in self.colors else "-"

    def rotate(self, face, direction):
        n = 4
        faces = []
        if face in [Face.FRONT, Face.BACK]:
            faces = [Face.TOP, Face.LEFT, Face.BOTTOM, Face.RIGHT]
        if face in [Face.RIGHT, Face.LEFT]:
            faces = [Face.TOP, Face.FRONT, Face.BOTTOM, Face.BACK]
        if face in [Face.TOP, Face.BOTTOM]:
            faces = [Face.FRONT, Face.RIGHT, Face.BACK, Face.LEFT]

        if face not in [Face.BACK, Face.LEFT, Face.BOTTOM]:
            faces.reverse()

        if direction == Direction.TURN_COUNTER_CLOCKWISE:
            faces.reverse()

        next_face = self.colors[faces[n - 1]]
        for i in range(n):
            tmp = self.colors[faces[i]]
            self.colors[faces[i]] = next_face
            next_face = tmp

    def __repr__(self):
        s = ""
        for face in self.colors:
            s += self.colors[face] if self.colors[face] is not None else "-"
        return s

    #def ran(self):




# ------------------------------------------------------

# ------------------------------------------------------
class Face:
    FRONT = 'front'
    BACK = 'back'
    RIGHT = 'right'
    LEFT = 'left'
    TOP = 'top'
    BOTTOM = 'bottom'

    def __init__(self, face, cells):
        self.face = face
        self.cells = cells

    def clone(self):
        return Face(self.face, deepcopy(self.cells))

    def _copy_cells(self):
        n = len(self.cells)
        cells = [[Cell().copy_from(self.cells[i][j]) for j in range(n)] for i in range(n)]
        return cells

    def turn(self, direction):
        n = len(self.cells)
        cells = self._copy_cells()
        # print(cells)
        for row in cells:
            for col in row:
                col.rotate(self.face, direction)
        # print(cells)

        if direction == Direction.TURN_CLOCKWISE:
            for i in range(n):
                for j in range(n):
                    self.cells[j][n - 1 - i].copy_from(cells[i][j])
        elif direction == Direction.TURN_COUNTER_CLOCKWISE:
            for i in range(n):
                for j in range(n):
                    self.cells[i][j].copy_from(cells[j][n - 1 - i])

    def serialize(self):
        s = ""
        for row in self.cells:
            for col in row:
                s += col.get_color(self.face)
        return s

    def __repr__(self):
        return self.serialize()

    def __str__(self):
        return self.serialize()
# ------------------------------------------------------


# ------------------------------------------------------
class Rubik:
    def __init__(self):
        self.size = 0
        self.cells = []
        self.faces = {}

    def standard(self):
        colors = "yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww"
        # colors = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz12"
        return self.from_serialize_str(colors)

    def construct(self, size=3):
        self.size = size
        self.cells = cells = [[[Cell() for _ in range(size)] for _ in range(size)] for _ in range(size)]
        near = 0
        rear = size - 1
        self.faces = {
            Face.TOP:
                Face(Face.TOP, [[cells[rear][size - 1 - y][x] for x in range(size)] for y in range(size)]),
            Face.LEFT:
                Face(Face.LEFT, [[cells[size - 1 - z][size - 1 - y][near] for y in range(size)] for z in range(size)]),
            Face.FRONT:
                Face(Face.FRONT, [[cells[size - 1 - z][near][x] for x in range(size)] for z in range(size)]),
            Face.RIGHT:
                Face(Face.RIGHT, [[cells[size - 1 - z][y][rear] for y in range(size)] for z in range(size)]),
            Face.BACK:
                Face(Face.BACK, [[cells[size - 1 - z][rear][size - 1 - x] for x in range(size)] for z in range(size)]),
            Face.BOTTOM:
                Face(Face.BOTTOM, [[cells[near][y][x] for x in range(size)] for y in range(size)]),
        }

    def from_serialize_str(self, colors_str):
        side = 6
        size = 2
        total = size ** 2 * side
        while total != len(colors_str):
            if total > len(colors_str):
                raise Exception('colors str not valid')
            size += 1
            total = size ** 2 * side
        self.construct(size)

        face_order = [Face.TOP, Face.LEFT, Face.FRONT, Face.RIGHT, Face.BACK, Face.BOTTOM]
        for face, colors_in_face in zip(face_order, re.findall('.' * (size ** 2), colors_str)):
            i = 0
            for row in re.findall('.' * size, colors_in_face):
                j = 0
                for col in row:
                    self.faces[face].cells[i][j].set_color(face, col)
                    j += 1
                i += 1
        return self

    def get_face(self, face):
        return self.faces[face]

    def clone(self):
        return Rubik().from_serialize_str(self.serialize())

    def serialize(self):
        s = ""
        for face in self.faces:
            s += repr(self.faces[face])
        return s

    def __repr__(self):
        return self.serialize()

    def __str__(self):
        return self.serialize()

    def compare_to(self, other):
        a = self.serialize()
        b = other.serialize()
        if len(a) != len(b):
            return float("inf")
        diff = 0
        for c1, c2 in zip(a,b):
            diff += 1 if c1 != c2 else 0
        return diff
# ------------------------------------------------------


# ------------------------------------------------------
class Action:
    def __init__(self, face, direction):
        self.face = face
        self.direction = direction

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "(" + self.face + "," + self.direction + ")"

    def exec(self, rubik):
        rubik.get_face(self.face).turn(self.direction)
        return rubik

    def exec_reverse(self, rubik):
        rubik.get_face(self.face).turn(self.direction)
        rubik.get_face(self.face).turn(self.direction)
        rubik.get_face(self.face).turn(self.direction)
        return rubik

    @staticmethod
    def all_possible_actions():
        return [
            Action(Face.TOP, Direction.TURN_CLOCKWISE),
            Action(Face.LEFT, Direction.TURN_CLOCKWISE),
            Action(Face.FRONT, Direction.TURN_CLOCKWISE),
            Action(Face.RIGHT, Direction.TURN_CLOCKWISE),
            Action(Face.BACK, Direction.TURN_CLOCKWISE),
            Action(Face.BOTTOM, Direction.TURN_CLOCKWISE),
            Action(Face.TOP, Direction.TURN_COUNTER_CLOCKWISE),
            Action(Face.LEFT, Direction.TURN_COUNTER_CLOCKWISE),
            Action(Face.FRONT, Direction.TURN_COUNTER_CLOCKWISE),
            Action(Face.RIGHT, Direction.TURN_COUNTER_CLOCKWISE),
            Action(Face.BACK, Direction.TURN_COUNTER_CLOCKWISE),
            Action(Face.BOTTOM, Direction.TURN_COUNTER_CLOCKWISE),
        ]

    def get_reverse_action(self):
        return Action(self.face,
                      Direction.TURN_CLOCKWISE
                      if self.direction == Direction.TURN_COUNTER_CLOCKWISE else Direction.TURN_COUNTER_CLOCKWISE
                      )
# ------------------------------------------------------


# ------------------------------------------------------
class RubikFacade:
    def __init__(self, rubik=None):
        self.rubik = rubik if rubik is not None else Rubik().standard()
        self.prolog = Prolog()
        self.prolog.consult("Random.pl")

    def isEmpty(self, lst):
        return len(lst) == 0

    def readResult(self, rList, var):
        read = list(rList)[0][var]
        pair = []
        for i in read:
            pair.append(str(i))
        return {pair[0]: pair[1]}

    def random(self, n=1):
        actions = []
        possible_action = Action.all_possible_actions()

        for _ in range(n):
            a = self.prolog.query("random_action(X)")
            actionDict = self.readResult(a, "X")
            f = list(actionDict.keys())[0]
            d = list(actionDict.values())[0]
            action = Action(eval(f),eval(d))
            action.exec(self.rubik)
            actions.append(action)
        return actions

    def convert(self,string):
        pass


    def top(self):
        return self._action(self.rubik.get_face(Face.TOP))

    def left(self):
        return self._action(self.rubik.get_face(Face.LEFT))

    def front(self):
        return self._action(self.rubik.get_face(Face.FRONT))

    def right(self):
        return self._action(self.rubik.get_face(Face.RIGHT))

    def back(self):
        return self._action(self.rubik.get_face(Face.BACK))

    def bottom(self):
        return self._action(self.rubik.get_face(Face.BOTTOM))

    def to_rubik(self):
        return self.rubik

    def _action(self, face):
        return ActionFacade(face)

    def _bcolor(self, color):
        if color == 'w':
            return '\033[107m  ' + '\033[0m'
        if color == 'y':
            return '\033[103m  ' + '\033[0m'
        if color == 'r':
            return '\033[101m  ' + '\033[0m'
        if color == 'b':
            return '\033[44m  ' + '\033[0m'
        if color == 'o':
            return '\x1b[6;30;43m  ' + '\033[0m'
        if color == 'g':
            return '\x1b[6;37;42m  ' + '\033[0m'
        if color is None:
            color = '-'
        return color + ','

    def __str__(self):
        plot = [[" " for _ in range(self.rubik.size * 4 + 4)] for _ in range(self.rubik.size * 3 + 3)]

        pos = {
            Face.TOP: (2 * self.rubik.size * 1 + 1, 0),
            Face.LEFT: (0, self.rubik.size * 1 + 1),
            Face.FRONT: (self.rubik.size * 1 + 1, self.rubik.size * 1 + 1),
            Face.RIGHT: (self.rubik.size * 2 + 2, self.rubik.size * 1 + 1),
            Face.BACK: (self.rubik.size * 3 + 3, self.rubik.size * 1 + 1),
            Face.BOTTOM: (2 * self.rubik.size * 1 + 1, self.rubik.size * 2 + 2),
        }

        for face in self.rubik.faces:
            si, sj = pos[face]
            for i in range(self.rubik.size):
                for j in range(self.rubik.size):
                    color = self.rubik.faces[face].cells[j][i].get_color(face)
                    plot[sj + j][si + i] = '' + self._bcolor(color)

        s = ""  # repr(self.cells) + '\n'
        for row in plot:
            for col in row:
                s += col if col is not None else "-"
            s += '\n'
        return s

    def __repr__(self):
        return repr(self.rubik)
# ------------------------------------------------------

# ------------------------------------------------------
class ActionFacade:
    def __init__(self, face):
        self.face = face

    def clockwise(self):
        self.face.turn(Direction.TURN_CLOCKWISE)

    def c(self):
        self.clockwise()

    def counter_clockwise(self):
        self.face.turn(Direction.TURN_COUNTER_CLOCKWISE)

    def cc(self):
        self.counter_clockwise()
# ------------------------------------------------------