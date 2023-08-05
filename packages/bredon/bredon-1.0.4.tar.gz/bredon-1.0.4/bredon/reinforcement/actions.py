from bredon.model import *
import random

class Action:
    def __init__(self, move, player):
        self.move = move
        try:
            self.color = player.color
        except:
            self.color = player

    def __repr__(self):
        return str(self.color) + ":" + str(self.move)

    @staticmethod
    def of(s):
        c, m = s.split(":")
        return Action(Move.of(m), Colors.of(c))

class Actions:
    def __init__(self, env):
        self.env = env

    def sample(self, player):
        return random.choice(list(self.env.get_actions(player)))