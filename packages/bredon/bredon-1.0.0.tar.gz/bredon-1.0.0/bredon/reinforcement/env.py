import gym
from bredon.model import *
from .actions import Action
import random
from bredon.view import *

class TakEnv(gym.Env):
    metadata = {'render.modes': ['ansi', 'human']}

    def __init__(self, size=5, players=None, board=None):
        self.size = size
        self.board = Board(size=size, board=board)
        self.players = players if players else []
        self.turn, self.move = 1, 1
        self.done = False
        self.vg = None

    def get_actions(self, player):
        return map(lambda i: Action(i, player), self.board.generate_valid_moves(self.turn, player.color, player.caps))

    def _step_turn(self):
        self.move = self.move % 2 + 1
        if self.move == 1:
            self.turn += 1

    def step(self, action):
        move = self.board.parse_move(action.move, action.color)
        if isinstance(move, PseudoBoard) and move.bool:
            self.board.force(move)
        else:
            for m in move:
                if isinstance(move, PseudoBoard) and move.bool:
                    self.board.force(m)
                else:
                    return False

        self._step_turn()
        s, r, d, i = (self.board.board,
                      self.board.evaluate(action.color),
                      self.board.winner(self.players),
                      {} # TODO: implement info
                     )
        if d:
            self.done = True
        return s, r, d, i

    def reset(self):
        self.board = Board(size=self.size)

    def render(self, mode='ansi'):
        if mode == 'ansi':
            print(str(self.board))
        elif mode == 'human':
            if not self.vg:
                self.vg = ViewGame(size=self.board.size, board=self.board, white=HUMAN, black=HUMAN)
            else:
                self.vg._init_gui(board=self.board)
                self.vg.viz()

    def close(self):
        self.board = None

    def seed(self, seed=None):
        random.seed(seed)
        return [seed]

    def add_player(self, p: Player):
        self.players.append(p)

class HypoEnv(TakEnv):
    def __init__(self, **kwargs):
        TakEnv.__init__(self, **kwargs)
        self.old_state = self.board.copy()
        
    def step(self, action):
        ret = super().step(action)
        self.old_state = self.board.copy()
        return ret
        
    def hypostep(self, action):
        return super().step(action)
    
    def unstep(self):
        self.board = self.old_state.copy()

def hypoenv(env: TakEnv):
    return HypoEnv(size=env.size, players=env.players, board=env.board.board)
