# Money simulation in Python
# see "#if ECONSIM" in command2.cpp

import money_constants as const
import globals as glob
from agent_class_definition import AgentClass
import random
import math

from matplotlib import pyplot as plt

def random_other_agent_with_stock_for_sale(buyer_idx): # done
    for ctr in range(1, 10):
        ans = random.randint(0, const.NUM_AGENTS-1)
        if ans != buyer_idx and agents[ans].stock_for_sale >= const.UNIT_OF_GOODS:
            return ans
    return const.NO_AGENT_FOUND

def average_current_selling_price():
    average = 0

    for agent in agents:
        average += agent.selling_price

    average /= const.NUM_AGENTS

    return average

def raw_wellbeing_from_savings(savings):
    x = savings / (average_current_selling_price() * const.TYPICAL_GOODS_MADE_PER_DAY)
    return -.9 + 2 / (1 + math.exp(-x)) + x * .05

def wellbeing_from_savings(agent_number, mod):
    agents[agent_number].num_days_savings_will_last = (agents[agent_number].our_money + mod) / \
            (average_current_selling_price() * const.TYPICAL_GOODS_MADE_PER_DAY)

    x = agents[agent_number].num_days_savings_will_last  # storing in 'x' to make the following equation look nicer

    return -.9 + 2 / (1 + math.exp(-x)) + x * .05

def select_agent_to_buy_from(purchasing_agent_idx):
    # collect SIZE_OF_SELECTION_LIST random other agents
    ans = const.NO_AGENT_FOUND
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

        ran = random.random() * sum_of_weights

        sum_so_far = 0

        for idx in range(0,len(small_list_of_other_agent_idxs)):
            sum_so_far += agent_list_weighting[idx]
            if sum_so_far >= ran:
                ans = small_list_of_other_agent_idxs[idx]
                break
        return ans
    else:
        return const.NO_AGENT_FOUND

    ###############################################

def wellbeing_from_consumption(agent_number, mod):
    x = agents[agent_number].goods_purchased + mod
    return x*.05+1/(1+math.exp(-(x-6)*1))

def wellbeing_from_consumption_and_savings(agent_number, modcon, modsav):
    return wellbeing_from_consumption(agent_number, modcon) * wellbeing_from_savings(agent_number, modsav)

def purchase():
    shuffled_agent_index_list = list(range(0, const.NUM_AGENTS))
    random.shuffle(shuffled_agent_index_list)

    for buying_agent_idx in shuffled_agent_index_list:
        if agents[buying_agent_idx].iterations_since_last_purchase > (agents[buying_agent_idx].days_between_purchases * const.ITERATIONS_PER_DAY):
            agents[buying_agent_idx].iterations_since_last_purchase = 0
            selling_agent_idx = select_agent_to_buy_from(buying_agent_idx)

            if selling_agent_idx == const.NO_AGENT_FOUND:
                pass
            else:
                agents[buying_agent_idx].num_units_purchased_on_last_shopping_trip = 0
                agents[buying_agent_idx].num_units_available_on_last_shopping_trip = (agents[selling_agent_idx].stock_for_sale / const.UNIT_OF_GOODS)
                num_purchases_made = 0
                while True:
                    purchase_made_flag = 0
                    # if we can afford to buy then decide if we would *like* to buy
                    if agents[buying_agent_idx].our_money >= (agents[selling_agent_idx].selling_price * const.UNIT_OF_GOODS):
                        wellbeing_now = wellbeing_from_consumption_and_savings(buying_agent_idx, 0, 0)
                        post_purchase_wellbeing = wellbeing_from_consumption_and_savings(
                            buying_agent_idx,
                            const.UNIT_OF_GOODS,
                            -agents[selling_agent_idx].selling_price * const.UNIT_OF_GOODS)

                        if (post_purchase_wellbeing > wellbeing_now):
                            purchase_made_flag = 1
                            num_purchases_made += 1

                            agents[buying_agent_idx].num_units_purchased_on_last_shopping_trip += 1

                            if (num_purchases_made > glob.greatest_ever_num_purchases_made):
                                glob.greatest_ever_num_purchases_made = num_purchases_made

                            if (num_purchases_made > 10000):
                                print("agent %d has made 10000 purchases - bug?", buying_agent)
                            # do the purchase


                            # they get less stock but more money

                            agents[selling_agent_idx].stock_for_sale -= const.UNIT_OF_GOODS
                            agents[selling_agent_idx].stock_sold_in_latest_iteration += const.UNIT_OF_GOODS

                            agents[selling_agent_idx].our_money += (agents[selling_agent_idx].selling_price * const.UNIT_OF_GOODS)
                            agents[selling_agent_idx].iterations_since_last_sell = 0
                            agents[selling_agent_idx].sales_since_last_price_change += 1

                            # we get more consumed but less money
                            agents[buying_agent_idx].goods_purchased += const.UNIT_OF_GOODS
                            agents[buying_agent_idx].goods_purchased_in_latest_iteration += 1
                            agents[buying_agent_idx].our_money -= (agents[selling_agent_idx].selling_price * const.UNIT_OF_GOODS)
                            agents[buying_agent_idx].iterations_since_last_buy = 0

                            last_observed_purchase_price = agents[selling_agent_idx].selling_price

                        # else report that we can't afford to purchase anything
                        else:
                            # print diagnostic?
                            pass

                        if purchase_made_flag and agents[selling_agent_idx].stock_for_sale >= const.UNIT_OF_GOODS:
                            # go round loop again and see if we should buy another one
                            pass
                        else:
                            break
        else:
            agents[buying_agent_idx].iterations_since_last_purchase += 1

def produce():
    for agent in agents:
        agent.stock_for_sale += (agent.goods_we_produce_per_day / const.ITERATIONS_PER_DAY)

def modify_prices():
    ### ALERT THIS WAS NOT THE BEST SOLUTION - command2.cpp contains a better one!
    ### ALERT THIS WAS NOT THE BEST SOLUTION - command2.cpp contains a better one!
    ### ALERT THIS WAS NOT THE BEST SOLUTION - command2.cpp contains a better one!
    ### ALERT THIS WAS NOT THE BEST SOLUTION - command2.cpp contains a better one!

    for agent in agents:
        if agent.stock_for_sale >= const.UNIT_OF_GOODS:
            agent.selling_price_multiplier = 1 + (agent.stock_for_sale - const.OPTIMAL_STOCK) * -.00005
            agent.selling_price *= agent.selling_price_multiplier

def consume():
    for agent in agents:
        agent.goods_purchased *= glob.one_day_half_life_multiplier

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

def do_all_plots():
    plt.subplot(4, 1, 1)
    plt.ylabel("Average selling price")
    plt.plot(list(range(glob.econ_iters_to_do_this_time)), history_of_average_current_selling_price, ",")

    plt.subplot(4, 1, 2)
    plt.ylabel(f"Agent[{agent_to_diagnose}] selling price")
    plt.plot(list(range(glob.econ_iters_to_do_this_time)), history_of_agents_price, ",")

    plt.subplot(4, 1, 3)
    plt.ylabel(f"Agent[{agent_to_diagnose}] stock for sale")
    plt.plot(list(range(glob.econ_iters_to_do_this_time)), history_of_agents_stock_for_sale, ",")
    plt.plot([0, glob.econ_iters_to_do_this_time], [const.OPTIMAL_STOCK, const.OPTIMAL_STOCK])
    plt.plot([0, glob.econ_iters_to_do_this_time], [const.MAXIMUM_STOCK, const.MAXIMUM_STOCK])

    plt.subplot(4, 1, 4)
    plt.ylabel(f"Agent[{agent_to_diagnose}] goods purchased")
    plt.plot(list(range(glob.econ_iters_to_do_this_time)), history_of_agents_goods_purchased, ",")

    plt.show()

agent_to_diagnose = 0

agents = []

for i in range(0, const.NUM_AGENTS):
    agents.append(AgentClass())

history_of_average_current_selling_price = []

history_of_agents_price = []
history_of_agents_stock_for_sale = []
history_of_agents_goods_purchased = []

print("glob.econ_iters_to_do_this_time :" + str(glob.econ_iters_to_do_this_time))
for i in range(0, glob.econ_iters_to_do_this_time):
    iterate()
    if math.fmod(i, 10) == 0:
        print(i)
    history_of_average_current_selling_price.append(average_current_selling_price())
    history_of_agents_price.append(agents[agent_to_diagnose].selling_price)
    history_of_agents_stock_for_sale.append(agents[agent_to_diagnose].stock_for_sale)
    history_of_agents_goods_purchased.append(agents[agent_to_diagnose].goods_purchased)

do_all_plots()


