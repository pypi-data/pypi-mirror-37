import random

from .utils import *

inf = float('inf')


class Player(object):
    def __init__(self, board, color, name=None):
        self.board = board
        self.color = color
        self.stones, self.caps = 0, 0
        self.name = self.color.name if name is None else name

    def _do(self, m: Move, c, f=True):
        move = self.board.parse_move(m, c)
        if isinstance(move, PseudoBoard):
            if move.bool:
                stone_type = m.stone
                stone, cap = False, False
                if stone_type in [FLAT, STAND]:
                    self.stones += 1
                    stone = True
                else:
                    self.caps += 1
                    cap = True
                caps, _stones = self.caps > self.board.caps, self.stones > self.board.stones
                if _stones and caps:
                    self.stones -= stone
                    self.caps -= cap
                    # TODO: End the game
                    self.board.end_game()
                elif (_stones and stone) or (caps and cap):
                    self.stones -= stone
                    self.caps -= cap
                    raise ValueError(f"Not enough pieces left")
                    # f"\tStones played: {self.stones}, Total: {self.board.stones}"
                    # f"\tCaps played: {self.caps}, Total: {self.board.caps}"
                    # f"Stone: {stone}, Cap: {cap}")
                elif f:
                    return self.board.force(move)
            else:
                # Move is illegal
                raise ValueError("Illegal Move")
        elif f:
            self.board.force(move)

    def do(self, m: Move):
        return self._do(m, self.color)

    def out_of_tiles(self):
        return self.caps >= self.board.caps and self.stones >= self.board.stones

    def _pick_move(self, turn, color, input_fn=input):
        while True:
            m = str_to_move(input_fn("Enter move: "))
            # try:
            v = self.board.copy().force_move(m, color)
            if v is None:
                return m, color
            else:
                print("Parsed move", m)
                input("Received error "+ v)
            # except Exception as e:
            #     print("Parsed move", m)
            #     print("Received error", e)

    def pick_move(self, turn, input_fn=input, out=False):
        return self._pick_move(turn, self.color, input_fn=input_fn)[0]

    def pick_opposing_move(self, turn, input_fn=input, out=False):
        return self._pick_move(turn, self.color.flip(), input_fn=input_fn)


class BaseAI(Player):
    def pick_move(self, turn, input_fn=input, out=False):
        return

class RandomAI(BaseAI):
    def pick_move(self, turn, input_fn=input, out=False):
        return random.choice(list(self.board.generate_valid_moves(self)))


class MinimaxAI(BaseAI):
    def __init__(self, board, color, depth=3):
        super().__init__(board, color)
        self.depth = depth

    def pick_opposing_move(self, turn, input_fn=input, out=False):
        # if self.board.valid_str("a1", self.color.flip()):
        #     return str_to_move("a1"), self.color.flip()
        # return str_to_move(ascii_lowercase[self.board.size - 1] + str(self.board.size)), self.color.flip()
        return self.pick_move(turn, input_fn=input_fn), self.color.flip()

    def pick_move(self, turn, input_fn=None, out=False) -> Move:
        moves = self.board.generate_valid_moves(turn, self.color, self.caps)
        best_eval = inf
        if self.depth % 2 == 1:
            best_eval *= -1
        best_move = None
        old_state = self.board.copy_board()
        alpha = -inf
        for move in moves:
            if out: print("Running move", move, "current alpha", alpha)
            self.board.execute(move, self.color)
            alpha = self.minimax(self.depth - 1, self.board, alpha, inf, True, self.color.flip(),
                                 self.board.copy_board(), turn, out=out) * 4
            ev = self.board.evaluate(self.color)
            alpha -= ev / 2
            if abs(alpha) > THRESHOLD:
                alpha *= -1
            self.board.set(old_state)
            if out: print("\t", ev, alpha, best_eval, best_move)
            if (self.depth % 2 == 1 and alpha >= best_eval) or (self.depth % 2 == 0 and alpha <= best_eval):
                best_eval = alpha
                best_move = move
                if out: print("\tsetting move")
        if out: input()
        return best_move

    def minimax(self, depth, board, alpha, beta, maximising, color, old_state, turn, out=False):
        if board.road() or board.flat_win():
            if maximising:
                return -MAX_N * depth
            else:
                return MAX_N * depth
        elif depth == 0:
            return board.evaluate(color)
        
        moves = board.generate_valid_moves(turn, color, self.caps)
        if maximising:
            b_eval = -inf
            for move in moves:
                board.execute(move, color)
                b_eval = max(b_eval, self.minimax(depth - 1, board, alpha, beta, not maximising, color.flip(),
                                                  board.copy_board(), turn, out=out))
                board.set(old_state)
                alpha = max(alpha, b_eval)
                if beta <= alpha:
                    if beta < -THRESHOLD:
                        return beta
                    return -beta
        else:
            b_eval = inf
            for move in moves:
                board.execute(move, color)
                b_eval = min(b_eval, self.minimax(depth - 1, board, alpha, beta, not maximising, color.flip(),
                                                  board.copy_board(), turn, out=out))
                board.set(old_state)
                beta = min(beta, b_eval)
                if beta <= alpha:
                    if beta < -THRESHOLD:
                        return beta
                    return -beta
        return b_eval
