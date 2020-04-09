'''

with colab = 0 the program pops up a window full of buttons and checkboxes made with tkinter
with colab = 1 the program skips that and only displays a matplotlib graph at the end

'''

colab = 0

if colab:
    print("This is the Colab version of the simulation - it comes without the setup dialog")
else:
    print("This version will not run on Colab!")

import math
from matplotlib import pyplot as plt
if not colab:
    from tkinter import *
    from tkinter.ttk import *  # needed for progress bar

from abm import *

def save_GUI_set_constants():
    file = open("GUI_const.txt","w")
    for key,value in data_for_creating_widgets_to_set_variables.items():
        file.write(key+"\n")
        file.write(str(value["var"])+"\n")

    for key,value in data_for_creating_graphs_to_show_checkboxes.items():
        file.write(key+"\n")
        file.write(str(value["show"].get())+"\n")

    file.close()

def load_GUI_set_constants():
    try:
        file = open("GUI_const.txt","r")
        for key,value in data_for_creating_widgets_to_set_variables.items():
            key_str = file.readline()
            val_str = file.readline()
            key_str = key_str.rstrip("\n\r")
            val_str = val_str.rstrip("\n\r")
            #print(f"key_str = [{key_str}] val_str = [{val_str }]")
            if isinstance(data_for_creating_widgets_to_set_variables[key_str]["var"], float):
                data_for_creating_widgets_to_set_variables[key_str]["var"] = float(val_str)
            else:
                val_str = val_str.split('.')[0]
                data_for_creating_widgets_to_set_variables[key_str]["var"] = int(val_str)

        for key,value in data_for_creating_graphs_to_show_checkboxes.items():
            key_str = file.readline()
            val_str = file.readline()
            key_str = key_str.rstrip("\n\r")
            val_str = val_str.rstrip("\n\r")
            data_for_creating_graphs_to_show_checkboxes[key_str]["default"] = int(val_str)
        file.close()
    except:
        pass

def read_variables_from_gui():
    # read variables from GUI
    global NUM_AGENTS
    global econ_iters_to_do_this_time
    global NUM_AGENTS_FOR_PRICE_COMPARISON
    global TYPICAL_STARTING_MONEY
    global TYPICAL_GOODS_MADE_PER_DAY
    global MAXIMUM_STOCK
    global TYPICAL_DAYS_BETWEEN_PRICE_CHANGES
    global TYPICAL_DAYS_BETWEEN_PURCHASES
    global TYPICAL_STARTING_PRICE

    check_ctr = 0

    shortname = "nc"; check_ctr += 1
    NUM_AGENTS_FOR_PRICE_COMPARISON       = data_for_creating_widgets_to_set_variables[shortname]["var"] = int(data_for_creating_widgets_to_set_variables[shortname]["box"].get())

    shortname = "na"; check_ctr += 1
    NUM_AGENTS                            = data_for_creating_widgets_to_set_variables[shortname]["var"] = int(data_for_creating_widgets_to_set_variables[shortname]["box"].get())

    shortname = "ni"; check_ctr += 1
    econ_iters_to_do_this_time            = data_for_creating_widgets_to_set_variables[shortname]["var"] = int(data_for_creating_widgets_to_set_variables[shortname]["box"].get())

    shortname = "sm"; check_ctr += 1
    TYPICAL_STARTING_MONEY                = data_for_creating_widgets_to_set_variables[shortname]["var"] = float(data_for_creating_widgets_to_set_variables[shortname]["box"].get())

    shortname = "gd"; check_ctr += 1
    TYPICAL_GOODS_MADE_PER_DAY            = data_for_creating_widgets_to_set_variables[shortname]["var"] = float(data_for_creating_widgets_to_set_variables[shortname]["box"].get())

    shortname = "ms"; check_ctr += 1
    MAXIMUM_STOCK                         = data_for_creating_widgets_to_set_variables[shortname]["var"] = float(data_for_creating_widgets_to_set_variables[shortname]["box"].get())

    shortname = "pc"; check_ctr += 1
    TYPICAL_DAYS_BETWEEN_PRICE_CHANGES    = data_for_creating_widgets_to_set_variables[shortname]["var"] = float(data_for_creating_widgets_to_set_variables[shortname]["box"].get())

    shortname = "bp"; check_ctr += 1
    TYPICAL_DAYS_BETWEEN_PURCHASES        = data_for_creating_widgets_to_set_variables[shortname]["var"] = float(data_for_creating_widgets_to_set_variables[shortname]["box"].get())

    shortname = "sp"; check_ctr += 1
    TYPICAL_STARTING_PRICE                = data_for_creating_widgets_to_set_variables[shortname]["var"] = float(data_for_creating_widgets_to_set_variables[shortname]["box"].get())

    assert(check_ctr == len(data_for_creating_widgets_to_set_variables))

    #for key,value in graphs_to_show.items()
    #    graphs_to_show[key]["default"] = graphs_to_show[key]["show"].get()

def shall_we_show_this_graph(short_description):
    if colab:
        answer = True
    else:
        answer = data_for_creating_graphs_to_show_checkboxes[short_description]["show"].get()
    return answer

def do_all_plots():
    if not colab:
        save_GUI_set_constants()
    # prep
    #plt.rcParams["figure.figsize"] = (18,12)

    plt.subplots_adjust(top=.98)
    plt.subplots_adjust(bottom=.02)
    plt.subplots_adjust(right=.98)
    plt.subplots_adjust(left=.07)

    # count selected graphs
    numrows = 0
    if colab:
        numrows += 9  # ??
    else:
        for val in data_for_creating_graphs_to_show_checkboxes.values():
            if val["show"].get():
                numrows += 1

    numrows += 1  # for the row of histograms at the bottom
    current_row = 1

    # show selected graphs
    if shall_we_show_this_graph("avsp"):
        plt.subplot(numrows,1,current_row)
        plt.ylabel("Average selling price")
        plt.plot(list(range(econ_iters_to_do_this_time)), history_of_average_current_selling_price, ",")
        current_row += 1

    if shall_we_show_this_graph("sp"):
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\nselling price")
        plt.plot(list(range(econ_iters_to_do_this_time)), history_of_agents_price, ",")
        current_row += 1

    if shall_we_show_this_graph("sfs"):
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\nstock for sale")
        axes = plt.gca()
        axes.set_ylim([0, max(max(history_of_agents_stock_for_sale), MAXIMUM_STOCK * 1.2)])
        plt.text(0, MAXIMUM_STOCK, "Max stock")
        plt.plot(list(range(econ_iters_to_do_this_time)), history_of_agents_stock_for_sale, ",")
        plt.plot([0, econ_iters_to_do_this_time], [MAXIMUM_STOCK, MAXIMUM_STOCK],color="#00ff00")
        start = -1
        for i in range(0, econ_iters_to_do_this_time):
            if history_of_agents_stock_for_sale[i] >= MAXIMUM_STOCK:
                if start == -1:
                    start = i
            if start >= 0 and history_of_agents_stock_for_sale[i] < MAXIMUM_STOCK:
               plt.plot([start, i], [MAXIMUM_STOCK, MAXIMUM_STOCK], color="#ff0000", linewidth=3)
               start = -1
        current_row += 1

    if shall_we_show_this_graph("dtfe"):
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\ndays till stock full/empty")
        axes = plt.gca()
        axes.set_ylim([0, 25])
        plt.plot(list(range(econ_iters_to_do_this_time)), history_of_agents_days_to_full, ",", color="#ff0000")
        plt.plot(list(range(econ_iters_to_do_this_time)), history_of_agents_days_to_empty, ",", color="#00ff00")
        current_row += 1

    if shall_we_show_this_graph("gp"):
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\ngoods purchased")
        plt.plot(list(range(econ_iters_to_do_this_time)), history_of_agents_goods_purchased, ",")
        current_row += 1

    if shall_we_show_this_graph("mon"):
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\nour money")
        plt.plot(list(range(econ_iters_to_do_this_time)), history_of_agents_our_money, ",")
        current_row += 1

    if shall_we_show_this_graph("wellmon"):
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\nwellbeing from money")
        plt.plot(list(range(econ_iters_to_do_this_time)), history_of_agents_well_money, ",")
        current_row += 1

    if shall_we_show_this_graph("wellcon"):
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\nwellbeing from consumption")
        plt.plot(list(range(econ_iters_to_do_this_time)), history_of_agents_well_coms, ",")
        current_row += 1

    if shall_we_show_this_graph("wellmoncon"):
        plt.subplot(numrows,1,current_row)
        plt.ylabel(f"Agent[{agent_to_diagnose}]\nwellbeing from mon+con")
        plt.plot(list(range(econ_iters_to_do_this_time)), history_of_agents_well_money_plus_cons, ",")
        current_row += 1

    # show histograms

    plt.subplot(numrows, 5, (numrows-1) * 5 + 1)
    plt.ylabel("Selling Price")
    plt.hist(all_prices_as_list, range=(0, max(all_prices_as_list) * 1.1), bins=20)

    plt.subplot(numrows, 5, (numrows-1) * 5 + 2)
    plt.ylabel("Stock for sale")
    plt.hist(stock_for_sale_as_list, range=(0, max(stock_for_sale_as_list) * 1.1), bins=20)

    plt.subplot(numrows, 5, (numrows-1) * 5 + 3)
    plt.ylabel("Money")
    plt.hist(our_money_as_list, range=(0, max(our_money_as_list) * 1.1), bins=20)

    plt.subplot(numrows, 5, (numrows-1) * 5 + 4)
    plt.ylabel("Purchased")
    plt.hist(num_units_purchased_on_last_shopping_trip_as_list, range=(0, max(num_units_purchased_on_last_shopping_trip_as_list) * 1.3), bins=20)

    plt.subplot(numrows, 5, (numrows-1) * 5 + 5)
    plt.ylabel("Available")
    plt.hist(num_units_available_on_last_shopping_trip_as_list, range=(0, max(num_units_available_on_last_shopping_trip_as_list) * 1.3), bins=20)

    plt.show()

def diagnostics():
    print("")
    print("---------------------------------------------------------------------")
    print("diagnostics():...")
    print(data_for_creating_widgets_to_set_variables)
    print("---------------------------------------------------------------------")

def update_progress_bar(i):
    if math.fmod(i, econ_iters_to_do_this_time / 100) == 0:
        progress_bar['value'] = float(i) / econ_iters_to_do_this_time * 100.0
        root.update_idletasks()

def run_model():
    plt.close()
    if colab:
        pass
    else:
        read_variables_from_gui()
        save_GUI_set_constants()

    initialise_model()

    for i in range(0, econ_iters_to_do_this_time):
        iterate()
        append_current_state_to_history()
        if not colab:
            update_progress_bar(i)

    collect_data_for_plotting_histograms()

    do_all_plots()

# prepare histograms

all_prices_as_list.clear()
stock_for_sale_as_list.clear()
our_money_as_list.clear()
num_units_purchased_on_last_shopping_trip_as_list.clear()
num_units_available_on_last_shopping_trip_as_list.clear()

# Begin creation of button/GUI window
if not colab:
    root = Tk()
    root.title("A Monetary System ABM")

data_for_creating_graphs_to_show_checkboxes =   {
                                                    "avsp": {"desc": "Average sell price",           "default": 1},
                                                      "sp": {"desc": "Selling price",              "default": 1},
                                                     "sfs": {"desc": "Stock for sale",          "default": 1},
                                                      "gp": {"desc": "Goods purchased",         "default": 1},
                                                     "mon": {"desc": "Our stock of money",               "default": 0},
                                                 "wellmon": {"desc": "Wellbeing money",         "default": 0},
                                                 "wellcon": {"desc": "Wellbeing from consumption",           "default": 0},
                                              "wellmoncon": {"desc": "Wellbeing from money + wellbeing from consumption",   "default": 0},
                                                    "dtfe": {"desc": "Days till empty / full",  "default": 0},
                                                }

data_for_creating_widgets_to_set_variables = {
                                                "na": {"desc": "Number of agents",                  "var": NUM_AGENTS},
                                                "sm": {"desc": "Typical starting money",            "var": TYPICAL_STARTING_MONEY},
                                                "nc": {"desc": "Num agents for price comparison",   "var": NUM_AGENTS_FOR_PRICE_COMPARISON},
                                                "ni": {"desc": "Num iterations to run",             "var": econ_iters_to_do_this_time},
                                                "gd": {"desc": "Typical goods made per Day",        "var": TYPICAL_GOODS_MADE_PER_DAY},
                                                "ms": {"desc": "Maximum stock",                     "var": MAXIMUM_STOCK},
                                                "pc": {"desc": "Typical days between price change", "var": TYPICAL_DAYS_BETWEEN_PRICE_CHANGES},
                                                "bp": {"desc": "Typical days between purchases",    "var": TYPICAL_DAYS_BETWEEN_PURCHASES},
                                                "sp": {"desc": "Typical starting price",            "var": TYPICAL_STARTING_PRICE}
                                             }

load_GUI_set_constants()

# make widgets to set variables

if colab:
    run_model()
else:
    row_ctr = 0
    for key, value in data_for_creating_widgets_to_set_variables.items():
        label = Label(root, text=value["desc"])
        label.grid(row=row_ctr, column=0, sticky=E, padx=5, pady=5)
        number_entry_box = Entry(root)
        number_entry_box.grid(row=row_ctr, column=1, padx=5, pady=5)
        number_entry_box.insert(0, value["var"])
        value["lab"] = label
        value["box"] = number_entry_box
        row_ctr += 1

    # make the graphs-to-display checkboxes
    frame_for_checkboxes = LabelFrame(root,text="Graphs to display")
    frame_for_checkboxes.grid(row=row_ctr, column=0, columnspan=2, padx=5, pady=5, sticky=W + E)

    for checkbox_row, (key, value) in enumerate(data_for_creating_graphs_to_show_checkboxes.items(), start=1):
        value["show"] = IntVar()
        value["show"].set(value["default"])

        label = Label(frame_for_checkboxes, text=value["desc"])
        label.grid(row=checkbox_row, column=0, sticky=E, padx=5, pady=5)

        check_box = Checkbutton(frame_for_checkboxes, variable=value["show"])
        check_box.grid(row=checkbox_row, column=1, padx=5, pady=5)

    refresh_button = Button(frame_for_checkboxes, text="Refresh graphs window", command=do_all_plots)
    refresh_button.grid(row=len(data_for_creating_graphs_to_show_checkboxes)+1, column=1, padx=5, pady=5)

    row_ctr += 1

    # progress bar and buttons
    progress_label = Label(root, text="Progress:")
    progress_label.grid(row=row_ctr, column=0, sticky=E, padx=5, pady=5)
    progress_bar = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
    progress_bar.grid(row=row_ctr, column=1, padx=5, pady=15)
    row_ctr += 1

    frame_for_action_buttons = Frame(root)
    frame_for_action_buttons.grid(row=row_ctr, column=0, columnspan=2, padx=5, pady=5, sticky=W + E)

    run_button = Button(frame_for_action_buttons, text="Run!", command=run_model)
    run_button.grid(row=0, column=0, padx=5, pady=5, sticky=W + E)

    ex_button = Button(frame_for_action_buttons, text="Exit", command=exit)
    ex_button.grid(row=0, column=1, padx=5, pady=5, sticky=W+E)

    diag_button = Button(frame_for_action_buttons, text="Debug", command=diagnostics)
    diag_button.grid(row=0, column=2, padx=5, pady=5, sticky=W+E)

    root.mainloop()
