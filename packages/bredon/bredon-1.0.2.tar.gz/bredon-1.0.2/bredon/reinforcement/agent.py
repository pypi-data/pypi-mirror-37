from .env import *
from ..model import *
from random import sample
from tqdm import *

class TakAgent(Player):
    def __init__(self, **kwargs):
        self.env = kwargs.pop("env")
        Player.__init__(self, **kwargs)

class HypoTakAgent(TakAgent):
    def __init__(self, **kwargs):
        # assert 1 == 'https://github.com/AxeldeRomblay/MLBox'
        self.depth = kwargs.pop("depth")
        self.env = kwargs.pop("env")
        self.other = None
        TakAgent.__init__(self, **kwargs)

    def flip_player(self, p):
        if p is self:
            return self.other
        return self

    def solve(self):
        if not self.other:
            self.other = [p for p in self.env.players if p is not self][0]
        # print("Solving!")
        actions = list(self.env.get_actions(self))
        self.rewards = {str(i): 0 for i in actions}
        hypo = hypoenv(self.env)
        for a in tqdm(actions):
            # print(a, end=': ')
            hypo.hypostep(a)
            self._solve(self.depth - 1, hypoenv(hypo), str(a), self.other) #, float("-inf"), float("inf"))
            # print(self.rewards[str(a)])
            hypo.unstep()
        return self.get_best_play()

    def get_best_play(self):
        # r = {j:i for i, j in self.rewards.items()}
        r = {}
        for i, j in self.rewards.items():
            r.setdefault(j, []).append(i)
        return r[max(r)]

    def _solve(self, depth, env, super_move, player): #, alpha, beta):
        # env.render()
        # input()
        if depth == 0: return
        actions = env.get_actions(player)
        n, c = 0, 0
        neg = player is not self
        for a in actions:
            try:
                s, r, d, i = env.hypostep(a)
                if r != 0:
                    # if neg:
                    #     r = -r
                    #     if r < beta:
                    #         beta = r
                    # elif r > alpha:
                    #     alpha = r
                    # if beta <= alpha:
                    #     # print("pruned!")
                    #     # if c != 0: self.rewards[super_move] += n / c
                    #     # return
                    #     break
                    n += r
                    c += 1
                    self._solve(depth - 1, hypoenv(env), super_move, self.flip_player(player)) #, alpha, beta)
                env.unstep()
            except TypeError as te: pass # invalid move
        if c != 0:
            self.rewards[super_move] += n / c

def make_agent(env, color, class_=TakAgent, **kwargs):
    return class_(env=env, color=color, board=env.board, **kwargs)

def main():
    env = TakEnv()
    env.add_player(make_agent(env, Colors.WHITE, depth=3))
    env.add_player(make_agent(env, Colors.BLACK, depth=3))

    env.reset()

    p1, p2 = env.players

    # env.step(Action(str_to_move("a1"), p1))
    # env.step(Action(str_to_move("b3"), p2))
    env.step(Action(str_to_move("a1"), p1))
    env.step(Action(str_to_move("a2"), p1))
    env.step(Action(str_to_move("a3"), p1))
    env.step(Action(str_to_move("a4"), p1))
    env.step(Action(str_to_move("b1"), p2))
    env.step(Action(str_to_move("c1"), p2))
    env.step(Action(str_to_move("d1"), p2))
    a = p2.solve()
    print(a)
    print(p2.rewards)
    '''
    while not env.done:
        env.render()
        env.step(Action.of(random.choice(p1.solve())))
        env.render()
        env.step(Action.of(random.choice(p2.solve())))
    '''
