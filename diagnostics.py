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

greatest_ever_num_purchases_made = 0

# declare arrays for histograms
all_prices_as_list = []
stock_for_sale_as_list = []
our_money_as_list = []
num_units_purchased_on_last_shopping_trip_as_list = []
num_units_available_on_last_shopping_trip_as_list = []



agent_to_diagnose = 0

def collect_data_for_plotting_histograms(agents):
    for agent in agents:
        all_prices_as_list.append(agent.selling_price)
        stock_for_sale_as_list.append(agent.stock_for_sale)
        our_money_as_list.append(agent.our_money)
        num_units_purchased_on_last_shopping_trip_as_list.append(agent.num_units_purchased_on_last_shopping_trip)
        num_units_available_on_last_shopping_trip_as_list.append(agent.num_units_available_on_last_shopping_trip)

def append_current_state_to_history(agents, avsp, rwfs, wfc, wfcas):
    history_of_average_current_selling_price.append(avsp)
    history_of_agents_price.append(agents[agent_to_diagnose].selling_price)
    history_of_agents_stock_for_sale.append(agents[agent_to_diagnose].stock_for_sale)
    history_of_agents_goods_purchased.append(agents[agent_to_diagnose].goods_purchased)
    history_of_agents_our_money.append(agents[agent_to_diagnose].our_money)
    history_of_agents_well_money.append(rwfs)
    history_of_agents_well_coms.append(wfc)
    history_of_agents_well_money_plus_cons.append(wfcas)
    history_of_agents_days_to_full.append(agents[agent_to_diagnose].days_till_stock_storage_full)
    history_of_agents_days_to_empty.append(agents[agent_to_diagnose].days_till_stock_storage_empty)

def clear_histories():
    for key,value in history_list.items():
        history_list[key]["list"].clear()

    all_prices_as_list.clear()
    stock_for_sale_as_list.clear()
    our_money_as_list.clear()
    num_units_purchased_on_last_shopping_trip_as_list.clear()
    num_units_available_on_last_shopping_trip_as_list.clear()
