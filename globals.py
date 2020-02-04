import money_constants as const
from math import exp
from math import log


econ_iters_to_do_this_time = 4000
one_day_half_life_multiplier = exp(log(.5) / const.ITERATIONS_PER_DAY);
last_observed_purchase_price = const.TYPICAL_STARTING_PRICE
greatest_ever_num_purchases_made = 0

