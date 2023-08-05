from .env import *
from .actions import *
from .agent import *

from gym.envs.registration import register

for i in range(3, 9):
    register(
        id=f'Tak{i}x{i}-v0',
        entry_point=TakEnv,
        kwargs={
            'size': i,
        }
    )