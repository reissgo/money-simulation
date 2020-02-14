import money_constants as const

from utils import *
from globals import *


class AgentClass:

    def __init__(self):
        self.goods_purchased = const.TYPICAL_GOODS_MADE_PER_DAY * approx_one() / 2
        self.goods_purchased_in_latest_iteration = 0
        self.stock_for_sale = const.MAXIMUM_STOCK * approx_one() / 2.0
        self.stock_sold_in_latest_iteration = 0
        self.goods_we_produce_per_day = TYPICAL_GOODS_MADE_PER_DAY * approx_one()
        self.our_money = TYPICAL_STARTING_MONEY * approx_one()
        self.num_days_savings_will_last = 0
        self.selling_price = TYPICAL_STARTING_PRICE * approx_one()
        self.selling_price_multiplier = 0
        self.days_till_stock_storage_full = -1.0  # -1 just means not set yet
        self.days_till_stock_storage_empty = -1.0  # -1 just means not set yet
        self.iterations_since_last_buy = 0
        self.iterations_since_last_sell = 0
        self.price_rank = 0
        self.iterations_since_last_price_change = 0
        self.iterations_since_last_purchase = 0
        self.sales_since_last_price_change = 0
        self.num_units_purchased_on_last_shopping_trip = 0
        self.num_units_available_on_last_shopping_trip = 0
        self.days_between_price_changes = approx_one() * TYPICAL_DAYS_BETWEEN_PRICE_CHANGES
        self.days_between_purchases = approx_one() * TYPICAL_DAYS_BETWEEN_PURCHASES

