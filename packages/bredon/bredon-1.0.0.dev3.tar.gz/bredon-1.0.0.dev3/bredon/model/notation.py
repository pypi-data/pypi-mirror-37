from .utils import *


class PTN:
    def __init__(self, turn=1):
        self.moves = []
        self.turn = turn

    def append(self, move):
        if (not self.moves) or len(self.moves[-1]) == 2:
            self.moves.append([move])
        else:
            self.moves[-1].append(move)

    def fill(self):
        if len(self.moves) > 1:
            return self.moves
        m = [move for ply in self.moves for move in ply]
        while len(m) < 2:
            m.append("")
        return [m]

    def get(self, turn, color: Colors):
        return self[turn][color.value]

    def clear(self):
        self.moves.clear()

    def __getitem__(self, turn):
        return self.moves[turn]

    def __repr__(self):
        return "PTN(%r)" % self.moves

    def __str__(self):
        return tabulate(self.fill(), tablefmt="plain",
                        headers=[i.name for i in Colors],
                        showindex=range(self.turn, len(self.fill())+self.turn))

    def __len__(self):
        return len(self.moves)

    def __iter__(self):
        if self.moves:
            return iter(self.moves)
        return iter([])


def parse_tps(tps):
    rows = [i.split(",") for i in tps.strip('[TPS"] ').split("/")]
    last, move, turn = rows[-1][-1].split()
    rows[-1][-1] = last
    fs, cs = [0, 0], [0, 0]
    for y, row in enumerate(rows):
        r = []
        for x, c in enumerate(row):
            if 'x' == c:
                r.append(Square(x, y))
            elif 'x' in c:
                r.extend([Square(x, y) for _ in range(int(c[1]))])
            else:
                tiles = []
                for stone in c[:-1]:
                    tiles.append(Tile(Colors(int(stone)-1), x=x, y=y))
                    fs[int(stone)-1] += 1
                if c[-1] in STONES:
                    tiles[-1].stone = c[-1]
                    if c[-1] == CAP:
                        cs[int(stone)-1] += 1
                else:
                    tiles.append(Tile(Colors(int(c[-1])-1), x=x, y=y))
                r.append(Square(x, y, tiles=tiles))
        rows[y] = r[:]
    board = list(zip(*reversed(rows)))
    for y, row in enumerate(board):
        for x, sq in enumerate(row):
            sq.x, sq.y = x, y
            for tile in sq.tiles:
                sq.fix(tile=tile)
    return Board(len(rows[0]), board=board), move, turn, [fs[0], cs[0]], [fs[1], cs[1]]
