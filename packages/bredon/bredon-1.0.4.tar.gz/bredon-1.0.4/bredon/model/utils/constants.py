import enum


# Colors
class Colors(enum.Enum):
    WHITE = 0
    BLACK = 1

    def flip(self):
        return Colors(1 - self.value)

    def __str__(self):
        return self.name  #[0]

    @staticmethod
    def of(s):
        return Colors[s]


# PTN
MARKS = '?!'

# Moves
DIRS = '+-<>'
UP, DOWN, LEFT, RIGHT = DIRS
STONES = 'FCS'
FLAT, CAP, STAND = STONES
EMPTY = ' '

# Graphics
TILE_SIZE   = 40
SQUARE_SIZE = 75
ANIM_STEPS  = 30
OFFSET_STEP = 3
PAD_STEP    = 5

# What a great coder
N, S, D = TILE_SIZE / 2, SQUARE_SIZE / 2, PAD_STEP

# AI
MAX_N = 1234567890
THRESHOLD = 10000

# Controller
HUMAN = "human", None
AI = lambda n: ("AI", n)

# Misc
SIZES = {
    3: [10, 0],
    4: [15, 0],
    5: [21, 1],
    6: [30, 1],
    7: [40, 2],
    8: [50, 2]
}
