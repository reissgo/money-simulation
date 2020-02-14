print("globals.py being imported - start")

from money_constants import *
from math import exp
from math import log


econ_iters_to_do_this_time = 20000
one_day_half_life_multiplier = exp(log(.5) / ITERATIONS_PER_DAY)
greatest_ever_num_purchases_made = 0

print("globals.py being imported - end")
