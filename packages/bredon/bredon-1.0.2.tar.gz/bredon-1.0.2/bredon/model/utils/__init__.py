from .constants import *

from collections   import namedtuple
from dataclasses   import dataclass, field
from functools     import partial
from itertools     import combinations, chain, starmap, repeat
from operator      import sub
from tabulate      import tabulate, re
from string        import ascii_lowercase
from random        import randint

PseudoBoard = namedtuple("PseudoBoard",
                         ("w", "h", "board", "bool", "err", "type"))


def sums(n):
    b, mid, e = [0], list(range(1, n)), [n]
    splits = (d for i in range(n) for d in combinations(mid, i))
    return (list(map(sub, chain(s, e), chain(b, s))) for s in splits)


def tile_to_coords(t: str):
    return int(t[1]) - 1, ascii_lowercase.index(t[0])


def coords_to_tile(x: int, y: int):
    return ascii_lowercase[y] + str(x + 1)


@dataclass
class Move:
    total: int = 1
    stone: str = FLAT
    col: str = None
    row: int = None
    moves: list = field(default_factory=list)
    direction: str = None

    def get_square(self):
        return self.col + str(self.row)

    def __repr__(self):
        return 'Move(' + ', '.join([f"{k}={v!r}" for k, v in self.__dict__.items()]) + ')'

    def __str__(self):
        if not self.direction:
            return (self.stone + self.get_square()).strip(FLAT)
        else:
            return str(self.total) + self.get_square() + self.direction + ''.join(map(str, self.moves))

    @staticmethod
    def of(s):
        return str_to_move(s)

class Next:
    __slots__ = 'x', 'y'

    def next(self, direction, size):
        if direction == LEFT and self.y > 0:
            return self.x, self.y - 1
        if direction == RIGHT and self.y < size - 1:
            return self.x, self.y + 1
        if direction == DOWN and self.x > 0:
            return self.x - 1, self.y
        if direction == UP and self.x < size - 1:
            return self.x + 1, self.y
        return self.x, self.y

    def tru_next(self, direction, size):
        if direction == DOWN and self.y > 0:
            return self.x, self.y - 1
        if direction == UP and self.y < size - 1:
            return self.x, self.y + 1
        if direction == RIGHT and self.x > 0:
            return self.x - 1, self.y
        if direction == LEFT and self.x < size - 1:
            return self.x + 1, self.y
        return self.x, self.y


@dataclass
class Tile(Next):
    color: str
    stone: str = FLAT
    x: int = None
    y: int = None

    def __repr__(self):
        return '%s{%s}' % (self.color, self.stone)  # + f'@{coords_to_tile(self.x, self.y)}'


class Square(Next):
    def __init__(self, x, y, tiles=None):
        self.x, self.y = x, y
        self.tiles = [] if tiles is None else tiles

    def fix(self, tile, x=None, y=None):
        if x is None:
            tile.x, tile.y = self.x, self.y
        else:
            tile.x, tile.y, self.x, self.y = x, y, x, y

    def add(self, tile: Tile):
        self.tiles.append(tile)
        self.fix(tile)
        return self

    def extend(self, tiles):
        for tile in tiles:
            self.fix(tile)
        self.tiles.extend(tiles)
        return self

    def remove_top(self, n_tiles: int):
        n = len(self.tiles) - n_tiles
        top = self.tiles[n:]
        self.tiles = self.tiles[:n]
        return top

    def connections(self, board):
        conns = 0
        s = len(board)
        for direction in DIRS:
            x, y = self.next(direction, s)
            t_next = board[y][x].tiles
            if t_next:
                t_next = t_next[-1]
                t = self.tiles
                if t:
                    t = t[-1]
                    if t_next is not t and \
                            t_next.color == t.color and t_next.stone in 'FC' and t.stone in 'FC':
                        conns += 1
        return conns

    def copy(self):
        return Square(self.x, self.y, tiles=self.tiles[:])

    def generate_tps(self):
        if len(self.tiles) == 0:
            return 'x'
        tps = ''.join(str(tile.color.value + 1) for tile in self.tiles)
        ending = self.tiles[-1].stone
        if ending in CAP + STAND:
            tps += ending
        return tps

    def __eq__(self, other):
        if other == EMPTY:
            return not bool(self.tiles)
        if isinstance(other, Square):
            return self.tiles == other.tiles
        if isinstance(other, Tile) and self.tiles:
            return self.tiles[-1] == other
        return False

    def __repr__(self):
        return ''.join(str(t) for t in self.tiles)  + f'@{coords_to_tile(self.x, self.y)}'


class Board:
    def __init__(self, size: int, board=None):
        self.size = size
        self.board = [[Square(x, y) for x in range(size)]
                      for y in range(size)] if board is None else board
        self.stones, self.caps = SIZES[size]

    def place(self, move: Move, curr_player):
        """
        Attempt to place the tile.
        Returns a PseudoBoard object.

        :param move
        :param curr_player
        :return nt was it placed?, board state
        """
        tile = Tile(curr_player, stone=move.stone)
        x, y = tile_to_coords(move.get_square())
        new_board = self.copy_board()
        if self.board[y][x] == EMPTY and \
                tile.x is None and tile.y is None:
            new_board[y][x].add(tile)
            return PseudoBoard(self.size, self.size, new_board, True, None, "place")
        return PseudoBoard(self.size, self.size, new_board, False, "Tile cannot be placed there", None)

    def move_single(self, old_square, new_square, n_tiles: int, first=False) -> PseudoBoard:
        """
        Move n_tiles from old_square to
        new_square.
        """
        if not isinstance(old_square, Square):
            if isinstance(new_square, tuple):
                old_square = self.get(*old_square)
            elif isinstance(new_square, str):
                old_square = self.get(*tile_to_coords(old_square))
        else:
            old_square = self.get(old_square.x, old_square.y)

        if not isinstance(new_square, Square):
            if isinstance(new_square, tuple):
                new_square = self.get(*new_square)
            elif isinstance(new_square, str):
                try:
                    new_square = self.get(*old_square.next(new_square, self.size))
                except ValueError:
                    return PseudoBoard(self.size, self.size, self.board, False,
                                       f"{old_square.x}, {old_square.y} is out of bounds for {new_square}", None)
            else:
                raise TypeError("new_square must be Square, tuple, or str, got: %s" % new_square.__class__)
        else:
            new_square = self.get(new_square.x, new_square.y)

        new_square = new_square.copy()
        old_square = old_square.copy()
        new_board = self.copy_board()
        if n_tiles <= len(old_square.tiles) - int(not first):
            valid = False
            flatten = False
            if len(new_square.tiles) == 0:
                valid = True
            else:
                new_stone = new_square.tiles[-1].stone
                old_stone = old_square.tiles[-1].stone
                if old_stone == CAP:
                    if new_stone == FLAT:
                        valid = True
                    elif new_stone == STAND and n_tiles == 1:
                        valid = True
                        flatten = True
                elif new_stone == FLAT:
                    valid = True
            if valid:
                new_board[new_square.y][new_square.x] = new_square.copy() \
                    .extend(old_square.remove_top(n_tiles))
                if flatten:
                    new_square.tiles[-1].stone = FLAT

                new_board[old_square.y][old_square.x] = old_square.copy()
                return PseudoBoard(self.size, self.size, new_board, True, None, "move")
            return PseudoBoard(self.size, self.size, new_board, False,
                               f"Tile is not flat: stone == {new_square.tiles[-1].stone}", None)
        return PseudoBoard(self.size, self.size, new_board, False,
                           f"Too many tiles: {n_tiles} > {len(old_square.tiles) - int(not first)}", None)

    def move(self, move: Move):
        copy = self.copy()
        sq = copy.get(*tile_to_coords(move.get_square()))
        yield self._run(lambda: copy.move_single(sq, move.direction, move.total, first=True), copy)
        for n in range(1, len(move.moves)):
            sq = copy.get(*sq.next(move.direction, self.size))
            yield self._run(lambda: copy.move_single(sq, move.direction, sum(move.moves[n:]), first=False), copy)

    def parse_move(self, move: Move, curr_player):
        if move.direction is None:
            return self.place(move, curr_player)
        else:
            return self.move(move)

    def force(self, pbs):
        if isinstance(pbs, PseudoBoard):
            return self.force([pbs])
        else:
            new_board = self.copy_board()
            for pb in pbs:
                if pb.err is not None:
                    return pb.err
                else:
                    new_board = pb.board
            self.board = new_board

    def force_move(self, s, curr_player):
        return self.force(self.parse_move(s, curr_player))

    def force_str(self, s, curr_player):
        return self.force(self.parse_move(str_to_move(s), curr_player))

    def valid(self, pbs):
        new_board = self.copy()
        return new_board.force(pbs) is None

    def valid_move(self, move, color):
        new_board = self.copy()
        return new_board.force_move(move, color) is None

    def valid_str(self, move, color):
        return self.valid_move(str_to_move(move), color)

    def winner(self, players, t=False):
        r = self.road()
        if r:
            return r
        elif all(sq != EMPTY for row in self.board for sq in row) or \
                any(player.out_of_tiles() for player in players):
            return self.flat_win(t=t, f=True)
        return None

    def flat_win(self, t=False, f=False):
        w, b = self.count_flats(Colors.WHITE), self.count_flats(Colors.BLACK)
        if f or all(len(sq.tiles) > 0 for row in self.board for sq in row):
            return ("TIE" if t else False) if w == b else Colors.WHITE if w > b else Colors.BLACK
        return False

    def road(self, out=False):
        for board in (self.board, zip(*self.board)):
            for color in Colors:
                if self._road_check(color, board, out=out):
                    return color
        return False

    def get(self, x: int, y: int) -> Square:
        return self.board[y][x]

    def copy_board(self):
        return [[s.copy() for s in r] for r in self.board]

    def copy(self):
        return Board(self.size, board=self.copy_board())

    def __repr__(self):
        return tabulate(self.board,
                        tablefmt="plain",
                        headers=list(range(1, self.size + 1)),
                        showindex=list(ascii_lowercase[:self.size]))

    def evaluate(self, color):
        return self._evaluate(color) - self._evaluate(color.flip())

    def execute(self, move, color):
        self.force_move(move, color)

    @classmethod
    def from_moves(cls, moves, size, colors=repeat(Colors.WHITE), stones=repeat(FLAT), board=None):
        b = cls(size) if board is None else board.copy()
        for m, s, c in zip(moves, stones, colors):
            b.force_str(s + m, c)
        return b

    def set(self, old_state):
        self.board = old_state

    def _valid(self, move, color):
        return self.valid(self.parse_move(move, color))

    def generate_valid_moves(self, turn, color, caps):
        return filter(lambda move: self._valid(move, color), self.generate_all_moves(turn, color, caps))

    def generate_all_moves(self, turn, color, caps):
        for y in range(self.size):
            for x in range(self.size):
                c, r = coords_to_tile(x, y)
                tile = self.get(x, y)
                if tile == EMPTY:
                    for stone in FLAT + STAND:
                        yield Move(stone=stone, col=c, row=r)
                    if caps < self.caps and turn > 1:
                        yield Move(stone=CAP, col=c, row=r)
                else:
                    if tile.tiles[-1].color == color:
                        for direction in DIRS:
                            try:
                                x1, y1 = tile.next(direction, self.size)
                                if 0 <= x1 < self.size and 0 <= y1 < self.size:
                                    for i in range(1, min(len(tile.tiles) + 1, self.size + 1)):
                                        if i == 1 and len(tile.tiles) == 1:
                                            yield Move(col=c, row=r, direction=direction)
                                        else:
                                            for moves in sums(i):
                                                if len(moves) == 1 and moves[0] == i:
                                                    yield Move(total=i, col=c, row=r, direction=direction)
                                                else:
                                                    yield Move(total=i, col=c, row=r, moves=moves, direction=direction)
                            except ValueError:
                                pass

    def generate_tps(self, turn=1, move=1):
        tps = '/'.join(','.join(map(Square.generate_tps, row)) for row in self.board)
        for i in range(self.size, 1, -1):
            tps = re.sub("(x,){%d}x" % i, "x" + str(i + 1), tps)
            tps = re.sub("(x,){%d}" % i, "x" + str(i) + ",", tps)

        return '[TPS "' + tps + '" %d %d]' % (turn, move)

    # STATIC PRIVATE HELPER METHODS
    def _run(self, fn, copy):
        try:
            pb = fn()
            copy.force(pb)
            return pb
        except IndexError as e:
            return PseudoBoard(self.size, self.size, [], False, e, None)

    def _evaluate_sq(self, color, sq):
        e = 0
        if sq.tiles:
            t = sq.tiles[-1]
            if t.color == color:
                e += sum(1 for i in sq.tiles if i.color == color and i.stone in 'CF') ** 5
                e += (sq.connections(self.board) + 1) ** 1.5
        return e

    def _evaluate(self, color):
        return sum(sum(map(partial(self._evaluate_sq, color), row)) for row in self.board) + \
               sum(map(len, self._compress_left(color, self.board, False))) ** 2 + \
               sum(map(len, self._compress_left(color, zip(*self.board), False))) ** 2

    def _cl_sq_check(self, r, color, out, sq):
        if out:
            print(r, color, sq)
        if sq.tiles and sq.tiles[-1].color == color:
            conns = sq.connections(self.board)
            return conns > 1 or ((r == 0 or r == self.size - 1) and conns > 0)
        return False

    def _cl_row_check(self, color, out, r, row):
        return list(filter(partial(self._cl_sq_check, r, color, out), row))

    def count_flats(self, color):
        return sum(1 for row in self.board for sq in row if sq.tiles and
                   sq.tiles[-1].color == color and sq.tiles[-1].stone == FLAT)

    def _compress_left(self, color, board, out):
        return list(starmap(partial(self._cl_row_check, color, out), enumerate(board)))

    def _road_check(self, color, board, out):
        road = self._compress_left(color, board, out)
        # if out:
        #     print(road)
        if road and (all(road) or
                     any(len(road[i]) >= self.size
                         for i in range(self.size))):
            return color
        return False

def str_to_move(move: str) -> Move:
    move_dir = None
    for direction in DIRS:
        if direction in move:
            move_dir = direction
            move = move.split(direction)
            break

    if move_dir is None:
        stone, c, r = move.zfill(3)
        return Move(stone=FLAT if stone == '0' else stone, col=c, row=r)
    else:
        ns = move[1]
        t = move[0]
        if t[0] not in ascii_lowercase:
            total = int(t[0])
            t = t[1:]
        else:
            total = 1
        c, r = t
        return Move(total=total, col=c, row=r, direction=move_dir, moves=list(map(int, ns)))
