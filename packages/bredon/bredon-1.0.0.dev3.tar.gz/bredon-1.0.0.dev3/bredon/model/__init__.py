from .notation import *
from .player   import *
from .utils    import *

def load_moves_from_file(filename, out=False):
    with open(filename) as file:
        ptn_str = file.read()
        _, s = ptn_str.split("Size")
        ptn_str = s.split("\n")
        size = int(s[2])
        b = Board(size)
        curr_player = Colors.WHITE
        ptn = PTN()
        for iturn, turn in enumerate(ptn_str[2:]):
            if 'R' in turn:
                break
            for imove, move in enumerate(turn.split(" ")[1:]):  # Exclude the round number
                if move:
                    if iturn == 0:
                        curr_player = [Colors.BLACK, Colors.WHITE][imove]
                    elif iturn == 1 and imove == 0:
                        curr_player = Colors.WHITE

                    b.force(b.parse_move(str_to_move(move), curr_player))

                    if out:
                        print(move)
                        print(str_to_move(move))
                        print(b)
                        print("Road?:", b.road())

                    if curr_player == Colors.BLACK:
                        curr_player = Colors.WHITE
                    else:
                        curr_player = Colors.BLACK
                    ptn.append(move)
                    yield b, move
    yield b, ptn

def exec_road(threat, size, return_size=False):
    """
    Threat types:
    1) column or row (straight) e.g. "a", "1"
    2) bent "{start}{start_dir}{bend-position}{new_dir}..." e.g.
        - c1+2<b+
    """

    b = Board(size)
    if len(threat) == 1:
        if threat in ascii_lowercase:
            return exec_road(threat + "1+", size)
        return exec_road("a" + threat + ">", size)
    srow, col, direction, *road = threat
    row, col = tile_to_coords(srow + col)

    sq = b.get(row, col)
    sqs = [coords_to_tile(sq.x, sq.y)]
    for bend, nd in zip(road[::2], road[1::2]):
        cond = True
        while cond:
            if direction in UP + DOWN:
                cond = sq.x < int(bend) - 1
            else:
                cond = sq.y < ascii_lowercase.index(bend)
            if not cond:
                direction = nd
            sq = b.get(*sq.next(direction, size))
            sqs.append(coords_to_tile(sq.x, sq.y))

    while True:
        nsq = b.get(*sq.next(direction, size))
        if (nsq.x, nsq.y) == (sq.x, sq.y):
            break
        sq = nsq
        sqs.append(coords_to_tile(sq.x, sq.y))

    if return_size:
        return sqs, size
    return sqs
