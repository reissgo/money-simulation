# Money simulation in Python
# see "#if ECONSIM" in command2.cpp

import money_constants as const
import globals as glob
from agent_class_definition import AgentClass
import random
import math
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from tkinter import *
from tkinter.ttk import *  # https://stackoverflow.com/questions/33768577/tkinter-gui-with-progress-bar

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

def raw_wellbeing_from_savings(savings):
    x = savings / (average_current_selling_price() * const.TYPICAL_GOODS_MADE_PER_DAY)
    return -.9 + 2 / (1 + math.exp(-x)) + x * .05

def wellbeing_from_savings(agent_number, mod):
    agents[agent_number].num_days_savings_will_last = (agents[agent_number].our_money + mod) / (average_current_selling_price() * const.TYPICAL_GOODS_MADE_PER_DAY)

    x = agents[agent_number].num_days_savings_will_last  # storing in 'x' to make the following equation look nicer

    return -.9 + 2 / (1 + math.exp(-x)) + x * .05

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
                num_purchases_made = False

                loop_counter = 0
                while True:
                    loop_counter += 1

                    #if loop_counter > 10000:
                    #   print(f"Oops!.. We found selling agent {selling_agent_idx} that currently has {agents[selling_agent_idx].stock_for_sale} for sale")
                    #    input("Pak")
                    purchase_made_flag = False
                    # if we can afford to buy then decide if we would *like* to buy
                    if agents[buying_agent_idx].our_money >= (agents[selling_agent_idx].selling_price * const.UNIT_OF_GOODS):
                        # we have enough money to buy goods from selling agent...
                        # haven't checked yet if we actually *want* to make the purchase

                        wellbeing_now = wellbeing_from_consumption_and_savings(buying_agent_idx, 0, 0)

                        post_purchase_wellbeing = wellbeing_from_consumption_and_savings(
                                                                                            buying_agent_idx,
                                                                                            const.UNIT_OF_GOODS,
                                                                                            -agents[selling_agent_idx].selling_price * const.UNIT_OF_GOODS)

                        if post_purchase_wellbeing > wellbeing_now:
                            purchase_made_flag = True
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

                        else:  # report that we can't afford to purchase anything
                            # print diagnostic?
                            assert purchase_made_flag is False

                        if purchase_made_flag and agents[selling_agent_idx].stock_for_sale >= const.UNIT_OF_GOODS:  # go round loop again and see if we should buy another one
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
        agent.stock_for_sale += (agent.goods_we_produce_per_day / const.ITERATIONS_PER_DAY)
        if agent.stock_for_sale > const.MAXIMUM_STOCK:
            agent.stock_for_sale = const.MAXIMUM_STOCK

def modify_prices():
    for agent in agents:

        agent.days_till_stock_storage_full = -1
        agent.days_till_stock_storage_full = -1




        if agent.iterations_since_last_price_change > (agent.days_between_price_changes * const.ITERATIONS_PER_DAY):

            #########
            sales_per_day = agent.sales_since_last_price_change * const.ITERATIONS_PER_DAY / max(1,
                                                                                                 agent.iterations_since_last_price_change)
            stock_growth_per_day = agent.goods_we_produce_per_day - sales_per_day

            # calc days_till_stock_storage_empty and days_till_stock_storage_full
            if stock_growth_per_day > 0:
                agent.days_till_stock_storage_full = (const.MAXIMUM_STOCK - agent.stock_for_sale) / stock_growth_per_day
            else:
                agent.days_till_stock_storage_full = const.INIFINITE

            if stock_growth_per_day < 0:
                agent.days_till_stock_storage_empty = agent.stock_for_sale / (-1 * stock_growth_per_day)
            else:
                agent.days_till_stock_storage_empty = const.INIFINITE
            #########


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

                elif agent.stock_for_sale < (const.MAXIMUM_STOCK / 2):  # // we can risk raising prices a smidge
                    agent.selling_price *= 1.05
                    agent.iterations_since_last_price_change = 0
                    agent.sales_since_last_price_change = 0

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

    # prep
    plt.rcParams["figure.figsize"] = (18,12)

    plt.subplots_adjust(top=.98)
    plt.subplots_adjust(bottom=.02)

    # count selected graphs
    numrows = 0
    for val in graphs_to_show.values():
        if val["show"].get():
            numrows += 1

    numrows += 1  # for the row of histograms at the bottom
    current_row = 1

    # show selected graphs
    if graphs_to_show["avsp"]["show"].get():
        plt.subplot(numrows,1,current_row)
        plt.ylabel("Average selling price")
        plt.plot(list(range(glob.econ_iters_to_do_this_time)), history_of_average_current_selling_price, ",")
        current_row += 1

    if graphs_to_show["sp"]["show"].get():
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\nselling price")
        plt.plot(list(range(glob.econ_iters_to_do_this_time)), history_of_agents_price, ",")
        current_row += 1

    if graphs_to_show["sfs"]["show"].get():
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\nstock for sale")
        axes = plt.gca()
        axes.set_ylim([0, max(max(history_of_agents_stock_for_sale), const.MAXIMUM_STOCK * 1.2)])
        plt.text(0, const.MAXIMUM_STOCK, "Max stock")
        plt.plot(list(range(glob.econ_iters_to_do_this_time)), history_of_agents_stock_for_sale, ",")
        plt.plot([0, glob.econ_iters_to_do_this_time], [const.MAXIMUM_STOCK, const.MAXIMUM_STOCK],color="#00ff00")
        start = -1
        for i in range(0, glob.econ_iters_to_do_this_time):
            if history_of_agents_stock_for_sale[i] >= const.MAXIMUM_STOCK:
                if start == -1:
                    start = i
            if start >= 0 and history_of_agents_stock_for_sale[i] < const.MAXIMUM_STOCK:
               plt.plot([start, i], [const.MAXIMUM_STOCK, const.MAXIMUM_STOCK], color="#ff0000", linewidth=3)
               start = -1
        current_row += 1

    if graphs_to_show["dtfe"]["show"].get():
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\ndays till stock full/empty")
        plt.plot(list(range(glob.econ_iters_to_do_this_time)), history_of_agents_days_to_full, ",", color="#ff0000")
        plt.plot(list(range(glob.econ_iters_to_do_this_time)), history_of_agents_days_to_empty, ",", color="#00ff00")
        current_row += 1

    if graphs_to_show["gp"]["show"].get():
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\ngoods purchased")
        plt.plot(list(range(glob.econ_iters_to_do_this_time)), history_of_agents_goods_purchased, ",")
        current_row += 1

    if graphs_to_show["mon"]["show"].get():
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\nour money")
        plt.plot(list(range(glob.econ_iters_to_do_this_time)), history_of_agents_our_money, ",")
        current_row += 1

    if graphs_to_show["wellmon"]["show"].get():
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\nwellbeing from money")
        plt.plot(list(range(glob.econ_iters_to_do_this_time)), history_of_agents_well_money, ",")
        current_row += 1

    if graphs_to_show["wellcon"]["show"].get():
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\nwellbeing from consumption")
        plt.plot(list(range(glob.econ_iters_to_do_this_time)), history_of_agents_well_coms, ",")
        current_row += 1

    if graphs_to_show["wellmoncon"]["show"].get():
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\nwellbeing from mon+con")
        plt.plot(list(range(glob.econ_iters_to_do_this_time)), history_of_agents_well_money_plus_cons, ",")
        current_row += 1

    # show histograms

    plt.subplot(numrows, 5, (numrows-1) * 5 + 1)
    plt.ylabel("Sell Price histo")
    assert(len(all_prices_as_list) > 0)
    plt.hist(all_prices_as_list, range=(0, max(all_prices_as_list) * 1.3), bins=20)

    plt.subplot(numrows, 5, (numrows-1) * 5 + 2)
    plt.ylabel("Stock histo")
    plt.hist(stock_for_sale_as_list, range=(0, max(stock_for_sale_as_list) * 5.3), bins=20)

    plt.subplot(numrows, 5, (numrows-1) * 5 + 3)
    plt.ylabel("money histo")
    plt.hist(our_money_as_list, range=(0, max(our_money_as_list) * 1.3), bins=20)

    plt.subplot(numrows, 5, (numrows-1) * 5 + 4)
    plt.ylabel("purch histo")
    plt.hist(num_units_purchased_on_last_shopping_trip_as_list, range=(0, max(num_units_purchased_on_last_shopping_trip_as_list) * 1.3), bins=20)

    plt.subplot(numrows, 5, (numrows-1) * 5 + 5)
    plt.ylabel("avail histo")
    plt.hist(num_units_available_on_last_shopping_trip_as_list, range=(0, max(num_units_available_on_last_shopping_trip_as_list) * 1.3), bins=20)

    plt.show()

def clear_histories():
    history_of_average_current_selling_price.clear()
    history_of_agents_price.clear()
    history_of_agents_stock_for_sale.clear()
    history_of_agents_goods_purchased.clear()
    history_of_agents_our_money.clear()
    history_of_agents_well_money.clear()
    history_of_agents_well_coms.clear()
    history_of_agents_well_money_plus_cons.clear()
    history_of_agents_days_to_full.clear()
    history_of_agents_days_to_empty.clear()
    all_prices_as_list.clear()
    stock_for_sale_as_list.clear()
    our_money_as_list.clear()
    num_units_purchased_on_last_shopping_trip_as_list.clear()
    num_units_available_on_last_shopping_trip_as_list.clear()

def run_model():

    plt.close()

    # read variables from GUI
    const.NUM_AGENTS_FOR_PRICE_COMPARISON       = int(var_widget_data_array["nc"]["box"].get())
    const.NUM_AGENTS                            = int(var_widget_data_array["na"]["box"].get())
    glob.econ_iters_to_do_this_time             = int(var_widget_data_array["ni"]["box"].get())
    const.TYPICAL_STARTING_MONEY                = float(var_widget_data_array["sm"]["box"].get())
    const.TYPICAL_GOODS_MADE_PER_DAY            = float(var_widget_data_array["gd"]["box"].get())
    const.MAXIMUM_STOCK                         = float(var_widget_data_array["ms"]["box"].get())
    const.TYPICAL_DAYS_BETWEEN_PRICE_CHANGES    = float(var_widget_data_array["pc"]["box"].get())
    const.TYPICAL_DAYS_BETWEEN_PURCHASES        = float(var_widget_data_array["bp"]["box"].get())
    const.TYPICAL_STARTING_PRICE                = float(var_widget_data_array["sp"]["box"].get())
    glob.last_observed_purchase_price = const.TYPICAL_STARTING_PRICE

    # create and initialise all agents
    agents.clear()

    for i in range(0, const.NUM_AGENTS):
        agents.append(AgentClass())

    clear_histories()
    for i in range(0, glob.econ_iters_to_do_this_time):
        iterate()

        if math.fmod(i, glob.econ_iters_to_do_this_time/100) == 0:
            progress_bar['value'] = float(i) / glob.econ_iters_to_do_this_time * 100.0
            root.update_idletasks()

        # keep running history of various things to plot at end

        history_of_average_current_selling_price.append(average_current_selling_price())
        history_of_agents_price.append(agents[agent_to_diagnose].selling_price)
        history_of_agents_stock_for_sale.append(agents[agent_to_diagnose].stock_for_sale)
        history_of_agents_goods_purchased.append(agents[agent_to_diagnose].goods_purchased)
        history_of_agents_our_money.append(agents[agent_to_diagnose].our_money)
        history_of_agents_well_money.append(raw_wellbeing_from_savings(agents[agent_to_diagnose].our_money))
        history_of_agents_well_coms.append(wellbeing_from_consumption(agent_to_diagnose,0))
        history_of_agents_well_money_plus_cons.append(wellbeing_from_consumption_and_savings(agent_to_diagnose,0,0))
        history_of_agents_days_to_full.append(agents[agent_to_diagnose].days_till_stock_storage_full)
        history_of_agents_days_to_empty.append(agents[agent_to_diagnose].days_till_stock_storage_empty)


        # go round loop again

    for agent in agents:
        all_prices_as_list.append(agent.selling_price)
        stock_for_sale_as_list.append(agent.stock_for_sale)
        our_money_as_list.append(agent.our_money)
        num_units_purchased_on_last_shopping_trip_as_list.append(agent.num_units_purchased_on_last_shopping_trip)
        num_units_available_on_last_shopping_trip_as_list.append(agent.num_units_available_on_last_shopping_trip)

    do_all_plots()


######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

agent_to_diagnose = 0

agents = []

# create arrays for storing histories of things we're going to monitor

# declare "history of" arrays
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

# declare arrays for histograms
all_prices_as_list = []
stock_for_sale_as_list = []
our_money_as_list = []
num_units_purchased_on_last_shopping_trip_as_list = []
num_units_available_on_last_shopping_trip_as_list = []

# prepare histograms

all_prices_as_list.clear()
stock_for_sale_as_list.clear()
our_money_as_list.clear()
num_units_purchased_on_last_shopping_trip_as_list.clear()
num_units_available_on_last_shopping_trip_as_list.clear()


# Begin creation of button/GUI window
root = Tk()
root.title("Agent Based Model")

row = 0
welcome_text_widget = Label(root, text="Welcome to Mick's Monetary Simulation")
welcome_text_widget.grid(row=row, column=0, columnspan=2, padx=5, pady=15)
row += 1

graphs_to_show = {
                        "avsp": {"desc": "Av sell price",           "default": 1},
                          "sp": {"desc": "Sell price",              "default": 1},
                         "sfs": {"desc": "Stock for sale",          "default": 0},
                          "gp": {"desc": "Goods purchased",         "default": 1},
                         "mon": {"desc": "Our money",               "default": 1},
                     "wellmon": {"desc": "Wellbeing money",         "default": 1},
                     "wellcon": {"desc": "Wellbeing con",           "default": 1},
                  "wellmoncon": {"desc": "Wellbeing money + con",   "default": 1},
                        "dtfe": {"desc": "Days till empty / full",  "default": 1},

}

var_widget_data_array = {
                            "na": {"desc": "Number of agents",                  "var": const.NUM_AGENTS},
                            "sm": {"desc": "Typical starting money",            "var": const.TYPICAL_STARTING_MONEY},
                            "nc": {"desc": "Num agents for price comparison",   "var": const.NUM_AGENTS_FOR_PRICE_COMPARISON},
                            "ni": {"desc": "Num iterations to run",             "var": glob.econ_iters_to_do_this_time},
                            "gd": {"desc": "Typical goods made per Day",        "var": const.TYPICAL_GOODS_MADE_PER_DAY},
                            "ms": {"desc": "Maximum stock",                     "var": const.MAXIMUM_STOCK},
                            "pc": {"desc": "Typical days between price change", "var": const.TYPICAL_DAYS_BETWEEN_PRICE_CHANGES},
                            "bp": {"desc": "Typical days between purchases",    "var": const.TYPICAL_DAYS_BETWEEN_PURCHASES},
                            "sp": {"desc": "Typical starting price",            "var": const.TYPICAL_STARTING_PRICE}
                        }

# make the label + text input fields
for key, value in var_widget_data_array.items():
    label = Label(root, text=value["desc"])
    label.grid(row=row, column=0, sticky=E, padx=5, pady=5)
    number_entry_box = Entry(root)
    number_entry_box.grid(row=row, column=1, padx=5, pady=5)
    number_entry_box.insert(0, value["var"])
    value["lab"] = label
    value["box"] = number_entry_box
    row += 1

# make the graphs to display checkboxes
frame_for_checkboxes = LabelFrame(root,text="Graphs to display")
frame_for_checkboxes.grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky=W+E)

cb_row = 1
for key, value in graphs_to_show.items():
    value["show"] = IntVar()
    value["show"].set(value["default"])

    label=Label(frame_for_checkboxes, text=value["desc"])
    label.grid(row=cb_row, column=0, sticky=E, padx=5, pady=5)

    check_box = Checkbutton(frame_for_checkboxes, variable=value["show"])
    check_box.grid(row=cb_row, column=1, padx=5, pady=5)

    cb_row += 1

refresh_button = Button(frame_for_checkboxes, text="Refresh", command=do_all_plots)
refresh_button.grid(row=cb_row, column=1, padx=5, pady=5)

row += 1


# progress bar and buttons
progress_label = Label(root, text="Progress:")
progress_label.grid(row=row, column=0, sticky=E, padx=5, pady=5)
progress_bar = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
progress_bar.grid(row=row, column=1, padx=5, pady=15)
row += 1

my_frame_at_bottom = Frame(root)
my_frame_at_bottom.grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky=W+E)

run_button = Button(my_frame_at_bottom, text="Run!", command=run_model)
run_button.grid(row=0, column=0, padx=5, pady=5, sticky=W + E)

ex_button = Button(my_frame_at_bottom, text="Exit", command=exit)
ex_button.grid(row=0, column=1, padx=5, pady=5, sticky=W+E)

root.mainloop()


