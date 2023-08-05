from .controller import *
from .model import *
from .neural import *
from .reinforcement import *
from .view import *

import click

def validate_type(ctx, param, value):
    t, *n = value.split(":")
    t = t.upper()
    if t[0] == "H" and t in "HUMAN":
        return HUMAN
    elif t[0] == "A" and t in "AI":
        try:
            return AI(int(n[0]))
        except ValueError:
            raise click.BadParameter("depth must be a valid integer")
    else:
        raise click.BadParameter("type must be either 'human' or 'ai'")


def validate_game(ctx, param, value):
    if not value.endswith("Game"):
        value += "Game"
    try:
        return globals()[value]
    except KeyError:
        raise click.BadParameter("must be TextGame or ViewGame")


def validate_size(ctx, param, value):
    if 3 <= value <= 8:
        return value
    raise click.BadParameter("size must be between 3 and 8")


@click.command()
@click.option("--game",  "-g", callback=validate_game, default="ViewGame",
              help="Type of game to play: [Text|View]Game", show_default=True)
@click.option("--size",  "-s", callback=validate_size, default=5,
              help="The size of the board", show_default=True)
@click.option("--white", "-w", callback=validate_type, default="human",
              help="Type of the white player, [h(uman)|a(i)]:depth", show_default=True)
@click.option("--black", "-b", callback=validate_type, default="ai:3",
              help="Type of the black player, [h(uman)|a(i)]:depth", show_default=True)
def run_game(game, size, white, black):
    game(size=size, white=white, black=black).run()
    test_notation()
    # unittest.main(exit=False)


def test_notation():
    print(parse_tps('[TPS "x3,12,2S/x,22S,22C,11,21/121,212,12,1121C,1212S/21S,1,21,211S,12S/x,21S,2,x2 1 26"]'))
    *moves, (b, ptn) = load_moves_from_file("test-game.ptn")
    print(b)
    print(str(ptn))


if __name__ == '__main__':
    run_game()