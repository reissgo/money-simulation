import matplotlib.patches as patches
from tkinter import *
from tkinter.ttk import *  # https://stackoverflow.com/questions/33768577/tkinter-gui-with-progress-bar
import money_constants as const
import globals as glob


def save_GUI_set_constants():
    file = open("GUI_const.txt","w")
    for key,value in var_widget_data_array.items():
        file.write(key+"\n")
        file.write(str(value["var"])+"\n")

    for key,value in graphs_to_show.items():
        file.write(key+"\n")
        file.write(str(value["show"].get())+"\n")

    file.close()

def load_GUI_set_constants():
    try:
        file = open("GUI_const.txt","r")
        for key,value in var_widget_data_array.items():
            key_str = file.readline()
            val_str = file.readline()
            key_str = key_str.rstrip("\n\r")
            val_str = val_str.rstrip("\n\r")
            #print(f"key_str = [{key_str}] val_str = [{val_str }]")
            if isinstance(var_widget_data_array[key_str]["var"], float):
                var_widget_data_array[key_str]["var"] = float(val_str)
            else:
                val_str = val_str.split('.')[0]
                var_widget_data_array[key_str]["var"] = int(val_str)

        for key,value in graphs_to_show.items():
            key_str = file.readline()
            val_str = file.readline()
            key_str = key_str.rstrip("\n\r")
            val_str = val_str.rstrip("\n\r")
            graphs_to_show[key_str]["default"] = int(val_str)
        file.close()
    except:
        pass


def do_all_plots():
    save_GUI_set_constants()
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
        axes = plt.gca()
        axes.set_ylim([0, 25])
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


def gui_main():
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
                             "sfs": {"desc": "Stock for sale",          "default": 1},
                              "gp": {"desc": "Goods purchased",         "default": 1},
                             "mon": {"desc": "Our money",               "default": 0},
                         "wellmon": {"desc": "Wellbeing money",         "default": 0},
                         "wellcon": {"desc": "Wellbeing con",           "default": 0},
                      "wellmoncon": {"desc": "Wellbeing money + con",   "default": 0},
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


    load_GUI_set_constants()

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

    # make the graphs-to-display checkboxes
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

    diag_button = Button(my_frame_at_bottom, text="Debug", command=diagnostics)
    diag_button.grid(row=0, column=2, padx=5, pady=5, sticky=W+E)

    root.mainloop()


