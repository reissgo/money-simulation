from random import gauss
from random import randint
from random import shuffle
import globals as glob
import money_constants as const


def approx_one():
    g = gauss(0,.1)
    maxrange = .3
    g = min(g, maxrange)
    g = max(g, -maxrange)
    return 1 + g


def random_agent():
    return randint(0, const.NUM_AGENTS-1)


def plus_or_minus_one():
    return -1 + (randint(0, 1) * 2)
