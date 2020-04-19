from random import gauss, shuffle, randint, random
from math import exp, log


TYPICAL_STARTING_PRICE = 2.0
ITERATIONS_PER_DAY = 1000
NUM_AGENTS = 30
NUM_AGENTS_FOR_PRICE_COMPARISON = 3      # i.e. we purchase from cheapest of N others
TYPICAL_GOODS_MADE_PER_DAY = 10.0
MAXIMUM_STOCK = TYPICAL_GOODS_MADE_PER_DAY*7
TYPICAL_STARTING_MONEY = 100.0
TYPICAL_DAYS_BETWEEN_PRICE_CHANGES = 3
TYPICAL_DAYS_BETWEEN_PURCHASES = 1
UNIT_OF_GOODS = 1.0
NO_AGENT_FOUND = -1
SHOW_SALES_INFO = False
INFINITE = 9999999

econ_iters_to_do_this_time = 20000
one_day_half_life_multiplier = exp(log(.5) / ITERATIONS_PER_DAY)
greatest_ever_num_purchases_made = 0

# create arrays for storing histories of things we're going to monitor

history_of_average_current_selling_price = []
history_of_agents_price = []
history_of_agents_stock_for_sale = []
history_of_agents_goods_purchased = []
history_of_agents_our_money = []
history_of_agents_well_money = []
history_of_agents_well_coms = []
history_of_agents_well_money_plus_cons = []
history_of_agents_days_to_full = []
history_of_agents_days_to_empty = []

# This history_list looks very similar to graphs_to_show - but not the same because some graphs may display multiple
# histories at the same time - so the number of items in the two lists may not be the same

history_list = {
                "acsp": {"list": history_of_average_current_selling_price,  "desc": "Av current selling price"},
                  "ap": {"list": history_of_agents_price,                   "desc": "agents_price"},
                 "sfs": {"list": history_of_agents_stock_for_sale,          "desc": "agents_stock_for_sale"},
                  "gp": {"list": history_of_agents_goods_purchased,         "desc": "agents_goods_purchased"},
                  "om": {"list": history_of_agents_our_money,               "desc": "agents_our_money"},
                  "wm": {"list": history_of_agents_well_money,              "desc": "agents_well_money"},
                  "wc": {"list": history_of_agents_well_coms,               "desc": "agents_well_coms"},
                 "wmc": {"list": history_of_agents_well_money_plus_cons,    "desc": "well_money_plus_cons"},
                 "dtf": {"list": history_of_agents_days_to_full,            "desc": "days_to_full"},
                 "dte": {"list": history_of_agents_days_to_empty,           "desc": "days_to_empty"}
                }

# declare arrays for histograms
all_prices_as_list = []
stock_for_sale_as_list = []
our_money_as_list = []
num_units_purchased_on_last_shopping_trip_as_list = []
num_units_available_on_last_shopping_trip_as_list = []

agent_to_diagnose = 0

agents = []  # declare that "agents" is a list type - it will get populated within "initialise_model()"

def approx_one():
    return 1 + (random()-0.5)/10.0


class AgentClass:

    def __init__(self):
        self.goods_purchased = TYPICAL_GOODS_MADE_PER_DAY * approx_one() / 2
        self.goods_purchased_in_latest_iteration = 0
        self.stock_for_sale = MAXIMUM_STOCK * approx_one() / 2.0
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
        self.sales_since_last_price_change = 0
        self.num_units_purchased_on_last_shopping_trip = 0
        self.num_units_available_on_last_shopping_trip = 0
        self.days_between_price_changes = approx_one() * TYPICAL_DAYS_BETWEEN_PRICE_CHANGES
        self.days_between_purchases = approx_one() * TYPICAL_DAYS_BETWEEN_PURCHASES
        self.iterations_since_last_price_change = randint(0, int(self.days_between_price_changes * ITERATIONS_PER_DAY))
        self.iterations_since_last_purchase = randint(0, int(self.days_between_purchases * ITERATIONS_PER_DAY))

def random_agent():
    return randint(0, NUM_AGENTS-1)


def random_other_agent_with_stock_for_sale(buyer_idx): # done
    for ctr in range(1, 10):
        ans = randint(0, NUM_AGENTS-1)
        if ans != buyer_idx and agents[ans].stock_for_sale >= UNIT_OF_GOODS:
            return ans
    return NO_AGENT_FOUND

def average_current_selling_price():
    average = 0

    for agent in agents:
        average += agent.selling_price

    average /= NUM_AGENTS

    return average

def select_agent_to_buy_from(purchasing_agent_idx):
    # collect SIZE_OF_SELECTION_LIST random other agents
    ans = NO_AGENT_FOUND
    size_of_selection_list = 4
    agent_list_weighting = []
    small_list_of_other_agent_idxs = []
    for r in range(0, size_of_selection_list):
        tries = 0
        while True:
            r = random_other_agent_with_stock_for_sale(purchasing_agent_idx)
            if r != purchasing_agent_idx and (small_list_of_other_agent_idxs.count(r) == 0):
                small_list_of_other_agent_idxs.append(r)
                break
            tries += 1
            if tries > 10:
                break

    if len(small_list_of_other_agent_idxs) > 0:
        max_price = 0
        for idx in small_list_of_other_agent_idxs:
            if agents[idx].selling_price > max_price:
                max_price = agents[idx].selling_price

        head = max_price * 1.2  # the bigger the multiplier the more equal the probs between all the agents

        sum_of_weights = 0
        for idx in small_list_of_other_agent_idxs:
            weight = head - agents[idx].selling_price
            agent_list_weighting.append(weight)
            sum_of_weights += weight

        ran = random() * sum_of_weights

        sum_so_far = 0

        for idx in range(0,len(small_list_of_other_agent_idxs)):
            sum_so_far += agent_list_weighting[idx]
            if sum_so_far >= ran:
                ans = small_list_of_other_agent_idxs[idx]
                break
        return ans
    else:
        return NO_AGENT_FOUND

    ###############################################

def raw_wellbeing_from_savings(savings):
    x = savings / (average_current_selling_price() * TYPICAL_GOODS_MADE_PER_DAY)
    return -.9 + 2 / (1 + exp(-x)) + x * .05

def wellbeing_from_savings(agent_number, mod):
    agents[agent_number].num_days_savings_will_last = (agents[agent_number].our_money + mod) / (average_current_selling_price() * TYPICAL_GOODS_MADE_PER_DAY)

    x = agents[agent_number].num_days_savings_will_last  # storing in 'x' to make the following equation look nicer

    return -.9 + 2 / (1 + exp(-x)) + x * .05

def wellbeing_from_consumption(agent_number, mod):
    x = agents[agent_number].goods_purchased + mod
    return x*.05+1/(1+exp(-(x-6)*1))

def wellbeing_from_consumption_and_savings(agent_number, modcon, modsav):
    return wellbeing_from_consumption(agent_number, modcon) * wellbeing_from_savings(agent_number, modsav)

def purchase():
    global greatest_ever_num_purchases_made  # for reason explained here: https://eli.thegreenplace.net/2011/05/15/understanding-unboundlocalerror-in-python
    shuffled_agent_index_list = list(range(0, NUM_AGENTS))
    shuffle(shuffled_agent_index_list)

    for buying_agent_idx in shuffled_agent_index_list:
        if agents[buying_agent_idx].iterations_since_last_purchase > (agents[buying_agent_idx].days_between_purchases * ITERATIONS_PER_DAY):
            agents[buying_agent_idx].iterations_since_last_purchase = 0
            selling_agent_idx = select_agent_to_buy_from(buying_agent_idx)

            if selling_agent_idx == NO_AGENT_FOUND:
                pass
            else:
                agents[buying_agent_idx].num_units_purchased_on_last_shopping_trip = 0
                agents[buying_agent_idx].num_units_available_on_last_shopping_trip = (agents[selling_agent_idx].stock_for_sale / UNIT_OF_GOODS)
                num_purchases_made = False

                loop_counter = 0
                while True:
                    loop_counter += 1

                    #if loop_counter > 10000:
                    #   print(f"Oops!.. We found selling agent {selling_agent_idx} that currently has {agents[selling_agent_idx].stock_for_sale} for sale")
                    #    input("Pak")
                    purchase_made_flag = False
                    # if we can afford to buy then decide if we would *like* to buy
                    if agents[buying_agent_idx].our_money >= (agents[selling_agent_idx].selling_price * UNIT_OF_GOODS):
                        # we have enough money to buy goods from selling agent...
                        # haven't checked yet if we actually *want* to make the purchase

                        wellbeing_now = wellbeing_from_consumption_and_savings(buying_agent_idx, 0, 0)

                        post_purchase_wellbeing = wellbeing_from_consumption_and_savings(
                                                                                            buying_agent_idx,
                                                                                            UNIT_OF_GOODS,
                                                                                            -agents[selling_agent_idx].selling_price * UNIT_OF_GOODS)

                        if post_purchase_wellbeing > wellbeing_now:
                            purchase_made_flag = True
                            num_purchases_made += 1

                            agents[buying_agent_idx].num_units_purchased_on_last_shopping_trip += 1

                            if (num_purchases_made > greatest_ever_num_purchases_made):
                                greatest_ever_num_purchases_made = num_purchases_made

                            if (num_purchases_made > 10000):
                                print("agent %d has made 10000 purchases - bug?", buying_agent)
                            # do the purchase


                            # they get less stock but more money

                            agents[selling_agent_idx].stock_for_sale -= UNIT_OF_GOODS
                            agents[selling_agent_idx].stock_sold_in_latest_iteration += UNIT_OF_GOODS

                            agents[selling_agent_idx].our_money += (agents[selling_agent_idx].selling_price * UNIT_OF_GOODS)
                            agents[selling_agent_idx].iterations_since_last_sell = 0
                            agents[selling_agent_idx].sales_since_last_price_change += 1

                            # we get more consumed but less money
                            agents[buying_agent_idx].goods_purchased += UNIT_OF_GOODS
                            agents[buying_agent_idx].goods_purchased_in_latest_iteration += 1
                            agents[buying_agent_idx].our_money -= (agents[selling_agent_idx].selling_price * UNIT_OF_GOODS)
                            agents[buying_agent_idx].iterations_since_last_buy = 0

                            #last_observed_purchase_price = agents[selling_agent_idx].selling_price

                        else:  # report that we can't afford to purchase anything
                            # print diagnostic?
                            assert purchase_made_flag is False

                        if purchase_made_flag and agents[selling_agent_idx].stock_for_sale >= UNIT_OF_GOODS:  # go round loop again and see if we should buy another one
                            # we just made a purchase, let's pass, i.e. go round the "while true" loop again
                            if loop_counter > 10000:
                                print(f"Go round again ... wellbeing_now={wellbeing_now} post_purchase_wellbeing={post_purchase_wellbeing}")
                            pass
                        else:
                            if loop_counter > 10000:
                                print(f"break")
                            break

                        if loop_counter > 10000:
                            print(f"??")
                    else:
                        # we simply can not afford to buy from seller
                        break;
        else:
            agents[buying_agent_idx].iterations_since_last_purchase += 1

def produce():
    for agent in agents:
        agent.stock_for_sale += (agent.goods_we_produce_per_day / ITERATIONS_PER_DAY)
        if agent.stock_for_sale > MAXIMUM_STOCK:
            agent.stock_for_sale = MAXIMUM_STOCK

def modify_prices():
    for agent in agents:

        agent.days_till_stock_storage_full = -1
        agent.days_till_stock_storage_empty = -1

        sales_per_day_as_measured_since_last_price_change = agent.sales_since_last_price_change * ITERATIONS_PER_DAY / max(1,
                                                                                             agent.iterations_since_last_price_change)
        stock_growth_per_day = agent.goods_we_produce_per_day - sales_per_day_as_measured_since_last_price_change

        # calc days_till_stock_storage_full/empty - only really needed after the "if" but calc here for diagnostics
        if stock_growth_per_day > 0:
            agent.days_till_stock_storage_full = (MAXIMUM_STOCK - agent.stock_for_sale) / stock_growth_per_day
        else:
            agent.days_till_stock_storage_full = INFINITE

        if stock_growth_per_day < 0:
            agent.days_till_stock_storage_empty = agent.stock_for_sale / (-1 * stock_growth_per_day)
        else:
            agent.days_till_stock_storage_empty = INFINITE

        if agent.iterations_since_last_price_change > (agent.days_between_price_changes * ITERATIONS_PER_DAY):

            if stock_growth_per_day > 0:  # stock room filling up
                if agent.days_till_stock_storage_full < 3:
                    agent.selling_price *= 0.85
                    agent.iterations_since_last_price_change = 0
                    agent.sales_since_last_price_change = 0

                if 3 >= agent.days_till_stock_storage_full > 5:           # // NEARLY FULL! - lower prices now!
                    agent.selling_price *= 0.96
                    agent.iterations_since_last_price_change = 0
                    agent.sales_since_last_price_change = 0

                if 5 <= agent.days_till_stock_storage_full < 20:          # // NEARLY FULL! - lower prices now!
                    agent.selling_price *= 0.99
                    agent.iterations_since_last_price_change = 0
                    agent.sales_since_last_price_change = 0

                if 20 >= agent.days_till_stock_storage_full < 40:          # // WON'T BEE FULL FOR AGES - raise prices!
                    agent.selling_price *= 1.02
                    agent.iterations_since_last_price_change = 0
                    agent.sales_since_last_price_change = 0

                if agent.days_till_stock_storage_full >= 40:              # // WON'T BEE FULL FOR AGES - raise prices!
                    agent.selling_price *= 1.03
                    agent.iterations_since_last_price_change = 0
                    agent.sales_since_last_price_change = 0

            if stock_growth_per_day < 0: # // stock room emptying
                if agent.days_till_stock_storage_empty < 3:           # // NEARLY
                    agent.selling_price *= 1.1
                    agent.iterations_since_last_price_change = 0
                    agent.sales_since_last_price_change = 0

                elif agent.stock_for_sale < (MAXIMUM_STOCK / 2):  # // we can risk raising prices a smidge
                    agent.selling_price *= 1.05
                    agent.iterations_since_last_price_change = 0
                    agent.sales_since_last_price_change = 0

def consume():
    for agent in agents:
        agent.goods_purchased *= one_day_half_life_multiplier

def clear_histories():
    for key,value in history_list.items():
        history_list[key]["list"].clear()

    all_prices_as_list.clear()
    stock_for_sale_as_list.clear()
    our_money_as_list.clear()
    num_units_purchased_on_last_shopping_trip_as_list.clear()
    num_units_available_on_last_shopping_trip_as_list.clear()

def initialise_model():
    # create and initialise all agents
    global agents
    agents.clear()

    agents = [AgentClass() for _ in range(NUM_AGENTS)]

    clear_histories()

def append_current_state_to_history():
    history_of_average_current_selling_price.append(average_current_selling_price())
    history_of_agents_price.append(agents[agent_to_diagnose].selling_price)
    history_of_agents_stock_for_sale.append(agents[agent_to_diagnose].stock_for_sale)
    history_of_agents_goods_purchased.append(agents[agent_to_diagnose].goods_purchased)
    history_of_agents_our_money.append(agents[agent_to_diagnose].our_money)
    history_of_agents_well_money.append(raw_wellbeing_from_savings(agents[agent_to_diagnose].our_money))
    history_of_agents_well_coms.append(wellbeing_from_consumption(agent_to_diagnose, 0))
    history_of_agents_well_money_plus_cons.append(wellbeing_from_consumption_and_savings(agent_to_diagnose, 0, 0))
    history_of_agents_days_to_full.append(agents[agent_to_diagnose].days_till_stock_storage_full)
    history_of_agents_days_to_empty.append(agents[agent_to_diagnose].days_till_stock_storage_empty)

def collect_data_for_plotting_histograms():
    for agent in agents:
        all_prices_as_list.append(agent.selling_price)
        stock_for_sale_as_list.append(agent.stock_for_sale)
        our_money_as_list.append(agent.our_money)
        num_units_purchased_on_last_shopping_trip_as_list.append(agent.num_units_purchased_on_last_shopping_trip)
        num_units_available_on_last_shopping_trip_as_list.append(agent.num_units_available_on_last_shopping_trip)

def iterate():
    for agent in agents:
        agent.goods_purchased_in_latest_iteration = 0
        agent.stock_sold_in_latest_iteration = 0

    purchase()
    produce()
    modify_prices()
    consume()

    for agent in agents:
        agent.iterations_since_last_buy += 1
        agent.iterations_since_last_sell += 1
        agent.iterations_since_last_purchase += 1
        agent.iterations_since_last_price_change += 1

