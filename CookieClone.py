import tkinter as tk
import json
from time import time
from os import path
from Packages import time_delta_display, display_num
from TkinterPackages import CreateToolTip
# TODO: Add upgrades
# TODO: Add restarting incentive (Ascend)
# TODO: Add scrollbar for smaller screens
# TODO: Achievements


class GameWindow:
    """
    Displays the information from the Player object
    """
    def __init__(self, master):
        self.master = root
        self.master.title("Cookie Clicker")

        # COOKIE FRAME
        self.frame_cookie = tk.Frame(master)
        self.frame_cookie.pack(side=tk.TOP, fill=tk.X)

        # Creates cookie button
        self.image = tk.PhotoImage(file="Cookie.png")
        self.cookie = tk.Button(self.frame_cookie, compound=tk.TOP, width=256, height=256,
                                image=self.image, command=self.ck_click)
        self.cookie.pack(padx=2, pady=2)
        self.cookie.image = self.image

        # Creates balance number
        self.bal_show = tk.Label(master, text="Balance: " + str(PLAYER.balance))
        self.bal_show.pack()

        # Runs the game tick if the player has purchased a building # May remove this for accurate run time
        self.save_counter = 0
        self.game_tick()
        # Creates cps number
        self.cps_show = tk.Label(master, text="Clicks per Second (cps): " + str(PLAYER.cps))
        self.cps_show.pack()
########################################################################################################################

        # SHOP FRAME
        self.frame_shop = tk.Frame(master)
        self.frame_shop.pack(side=tk.TOP, fill=tk.X)

        # Creates shop grid
        self.label = tk.Label(self.frame_shop, text="################# Shop #################")
        self.label.grid(columnspan=3)

        # Creates shop titles
        self.shop_title_list = ["price", "building", "quantity"]
        for i, entry in enumerate(self.shop_title_list):
            self.entry = tk.Label(self.frame_shop, text=entry.capitalize())
            self.entry.grid(row=1, column=i)

        self.frame_mult = tk.Frame(self.frame_shop)
        self.frame_mult.grid(row=2, column=1)

        # Creates buy multipliers
        i = 0
        self.var = tk.IntVar()
        self.var.set(1)

        radio_list = [("1x", 1),
                      ("10x", 10),
                      ("100x", 100)]
        for name, val in radio_list:
            self.name = tk.Radiobutton(self.frame_mult, text=name, variable=self.var,
                                       value=val, indicatoron=0, width=5, command=self.create_shop)
            self.name.grid(row=0, column=i)
            i += 1

        self.count_list = []
        self.price_list = []
        self.button_lst = []
        self.tooltp_lst = []
        self.create_shop()
########################################################################################################################

        # MISC FRAME
        self.frame_misc = tk.Frame(master)
        self.frame_misc.pack(side=tk.TOP, fill=tk.X)

        # Creates grid
        self.label = tk.Label(self.frame_shop, text="################# Misc #################")
        self.label.grid(columnspan=4)

        # Creates Misc Buttons
        self.misc_list = (("Export Save", PLAYER.export_save, 0),
                          ("Import Save", PLAYER.import_save, 1),
                          ("Stats", self.stats_win, 2),
                          (" ", None, 3))
        for text, comm, c in self.misc_list:
            self.button = tk.Button(self.frame_misc, width=15, text=text, command=comm)
            self.button.grid(row=1, column=c)

    def create_shop(self):
        """
        Creates the entire shop: Prices, Buy buttons, & Quantity numbers based on PLAYER.inventory
        :return:
        """
        self.price_list = []
        self.button_lst = []
        self.count_list = []
        index = 1
        r = 3
        for building in PLAYER.inventory:
            label = building.name.lower().capitalize()

            # makes price labels (for the displayed price: is the price x [1.15^(building mult number-1)]
            # The '...-1' is because the correct price is stored in the PLAYER.inv entry
            price_name = tk.Label(self.frame_shop, width=21,
                                  text='$' +
                                       display_num(round(self.buy_ct_calculator(building.base_price, building.count))))
            price_name.grid(row=r)
            self.price_list.append(price_name)

            # makes purchase buttons
            but_name = tk.Button(self.frame_shop, text=label, width=20, command=lambda j=index: self.buy(j))
            but_name.grid(row=r, column=1)
            self.button_lst.append(but_name)

            # makes the rollover tooltips
            self.create_tooltip(building.name, building, index - 1)

            # makes count labels
            key = tk.Label(self.frame_shop, width=21, text=str(building.count))
            key.grid(row=r, column=2)
            self.count_list.append(key)

            r += 1
            index += 1

    def create_tooltip(self, name, building, index):
        """
        Creates tooltips
        :param name:
        :param building:
        :param index:
        :return:
        """
        label = name.capitalize()
        # Gets the cps created by the building type
        build_cps = building.count * building.cps
        PLAYER.cps_update()
        # Gets the % of the cps contributed by the building type
        try:
            build_cps_ratio = str(round(build_cps / PLAYER.cps * 100, 1))
        except ZeroDivisionError:
            build_cps_ratio = str(0.0)

        # Creates the tooltip
        CreateToolTip(self.button_lst[index],
                      "--Each " + label + " produces " + display_num(building.cps) + " cookies per second\n" +
                      "--" + display_num(building.count) + " " + label + "s producing " +
                      display_num(build_cps) + " cookies per second (" + build_cps_ratio + "%)")

    def ck_click(self):
        """
        If the player clicks the cookie, add a cookie and update the balance
        :return:
        """
        PLAYER.balance += 1
        PLAYER.earned += 1
        PLAYER.handmade += 1
        self.bal_show.config(text="Balance: " + str(display_num(round(PLAYER.balance))))

    def buy(self, choice):
        """
        Runs the backend for purchasing buildings
        :param choice:
        :return:
        """
        # Sets the variables for the function
        buy_ct = self.var.get()
        building = PLAYER.inventory[choice-1]
        # If the player can afford the building at it's current price based on quantity purchased
        if PLAYER.balance >= self.buy_ct_calculator(building.base_price, building.count):
            # For every copy of the building required...
            for i in range(0, buy_ct):
                # Take the cookies from the player
                PLAYER.balance -= building.current_price
                # Give the player one building
                building.count += 1
                # Raise the price of the next building
                building.current_price = self.buy_ct_calculator(building.base_price, building.count)
            # Update their balance
            bal = display_num(round(PLAYER.balance))
            self.bal_show.config(text="Balance: " + bal)
            # Update the building's count list
            self.count_list[choice - 1].config(text=display_num(building.count))
            # Update the building's price list
            self.price_list[choice - 1].config(text='$' +
                                                    display_num(round(building.current_price * (1.15 ** (buy_ct - 1)))))
            # Recalculate and update the cps
            PLAYER.cps_update()
            self.cps_show.config(text="Clicks per Second (cps): " + display_num(PLAYER.cps))

            # Update all the tooltips (for cps%)
            i = 0
            for entry in PLAYER.inventory:
                self.create_tooltip(entry.name, entry, i)
                i += 1

    def game_tick(self):
        """
        Adds the amount of cookies the player should receive every second
        :return:
        """
        # Ensure the cps is correct, uses the cps / 100 to make the bal update live, while using 1sec as the baseline
        PLAYER.cps_update(game_tick=1)
        # Add the cps to the player's balance
        PLAYER.balance += PLAYER.cps
        PLAYER.earned += PLAYER.cps
        # Update the balance
        self.bal_show.config(text="Balance: " + display_num(round(PLAYER.balance)))
        self.save_counter += 1
        if self.save_counter % 30000 == 0:
            self.save_counter = 0
            PLAYER.export_save()
        # Repeat after 10ms
        self.bal_show.after(10, self.game_tick)

    def buy_ct_calculator(self, base, build_ct):
        """
        Calculates the final cost of a building if the player is buying $buy_ct of them with $num being the current price
        :param num:
        :return:
        """
        buy_ct = self.var.get()
        return (base * (1.15**(build_ct + buy_ct) - 1.15**build_ct))/.15

    # noinspection PyAttributeOutsideInit
    def stats_win(self):
        self.app = self.Stats(tk.Toplevel(self.master))

    # noinspection PyUnresolvedReferences
    class Stats:
        def __init__(self, master):
            PLAYER.stats = {'balance': display_num(round(PLAYER.balance)),
                            'earned': display_num(round(PLAYER.earned)),
                            'lifetime': display_num(round(PLAYER.life_earned)),
                            'cps': display_num(round(PLAYER.cps * 100)),
                            'init_time': PLAYER.start_time,
                            'building count': PLAYER.building_ct,
                            'click strength': PLAYER.click_str,
                            'handmade': display_num(PLAYER.handmade)}
            self.label = tk.Label(master, text="################# Stats #################")
            self.label.grid(columnspan=2)

            r = 1
            for key in PLAYER.stats:
                if key == 'inventory' or key == 'pause_time':
                    continue
                if key == 'init_time':
                    self.key = tk.Label(master, text="Time Passed")
                    self.key.grid(row=r)
                    self.info = tk.Label(master, text=time_delta_display(time() - PLAYER.stats[key]))
                    self.info.grid(row=r, column=1)
                    r += 1
                    continue
                self.key = tk.Label(master, text=key.capitalize())
                self.key.grid(row=r)
                self.info = tk.Label(master, text=PLAYER.stats[key])
                self.info.grid(row=r, column=1)
                r += 1


########################################################################################################################


# noinspection PyUnresolvedReferences
class Player:
    """
    Handles all components of the game related to what the player owns
    Ex. Inventory, balance, stats, importing and exporting the previous, etc
    """
    def __init__(self):
        # Stores the balance in the bank
        self.balance = 0
        # Stores the balance earned this run
        self.earned = 0
        # Stores the lifetime balance (Ascend needed)
        self.life_earned = 0
        self.building_list = [
            ('auto clicker', .1, 15),
            ('grandma', 1, 100),
            ('farm', 8, 1100),
            ('mine', 47, 12000),
            ('factory', 260, 130000),
            ('bank', 1400, 1.4*10**6),
            ('temple', 7800, 2*10**7),
            ('wizard tower', 44000, 3.3*10**8),
            ('shipment', 260000, 5.1*10**9),
            ('alchemy lab', 1.6*10**6, 7.5*10**10),
            ('portal', 1*10**7, 1*10**12),
            ('time machine', 6.5*10**7, 1.4*10**13),
            ('anti-matter condenser', 4.3*10**8, 1.7*10**14),
            ('prism', 2.9*10**9, 2.1*10**15),
            ('chance maker', 2.1*10**10, 2.6*10**16),
            ('fractal engine', 1.5*10**11, 3.1*10**17)
        ]
        # Stores the buildings, their count, their cps, and their price
        self.inventory = []
        self.j_inv = []
        for entry in self.building_list:
            self.inventory.append(Building(*entry, 0, entry[2]))
        # Initializes the cookies per second (cps)
        self.cps = 0
        # Initializes the start time of the entire game
        self.start_time = time()
        # Initializes the start time of the session
        self.pause_time = 0
        # Sets the total number of owned buildings
        self.building_ct = 0
        # Sets the number of cookies per click (Upgrades needed)
        self.click_str = 1
        # Stores the number of clicked cookies
        self.handmade = 0
        # Stores the complete PLAYER object for backup and stats screen
        self.stats = {'balance': self.balance,
                      'earned': self.earned,
                      'lifetime': self.life_earned,
                      'cps': self.cps,
                      'init_time': self.start_time,
                      'pause_time': self.pause_time,
                      'building count': self.building_ct,
                      'click strength': self.click_str,
                      'handmade': self.handmade,
                      'inventory': self.inventory}

    def cps_update(self, game_tick=0):
        """
        Updates the player's cps based on inventory
        :return:
        """
        self.cps = 0
        # for every building in the inventory...
        for building in self.inventory:
            # If the calculation isn't for the game logic...
            if not game_tick:
                # the cps is the sum of the number of buildings multiplied by their cps value
                self.cps += building.count * building.cps
            # if the calculation is for the actual game logic...
            elif game_tick == 1:
                # the cps of each building is 1/100 the advertised value b/c the game tick happens every 1/100 seconds
                self.cps += building.count * (building.cps/100)

    def building_sum(self):
        total = 0
        for building in self.inventory:
            total += building.count
        return total

    def export_save(self):
        """
        Creates a save file with all of the information needed to reload the game
        :return:
        """
        print("Starting save...")
        self.j_inv = []
        # The program will use this time to calculate the time passed for the sleep cookies to e calculated
        for entry in self.inventory:
            self.j_inv.append(vars(entry))
        # Loads the stats dict to commit to the save
        # Stores the entire dict even though we don't need it to maintain the structure for the stats page
        self.stats = {'balance': self.balance,
                      'earned': self.earned,
                      'lifetime': self.life_earned,
                      'cps': self.cps_update(),
                      'init_time': self.start_time,
                      'pause_time': time(),
                      'building count': self.building_sum(),
                      'click_str': self.click_str,
                      'handmade': self.handmade,
                      'inventory': self.j_inv}
        # Opens the save file and writes the new save to it
        with open("CookieClone Save", "w", encoding="utf-8") as file:
            json.dump(self.stats, file, ensure_ascii=False, indent=2)
        print("Finished!")

    def import_save(self):
        """
        Reads and reloads the game with data from the save file
        :return:
        """
        print("Loading save...")
        # Extracts the stats dict from the saved JSON
        with open("CookieClone Save", "r", encoding="utf-8") as file:
            self.stats = json.load(file)

        # Extracts the data from the stats dict to populate the game
        self.balance = self.stats['balance']
        self.earned = self.stats['earned']
        self.life_earned = self.stats['lifetime']
        self.start_time = self.stats['init_time']
        self.pause_time = self.stats['pause_time']
        self.click_str = self.stats['click_str']
        self.handmade = self.stats['handmade']
        self.j_inv = self.stats['inventory']

        self.inventory = []
        for entry in self.j_inv:
            self.inventory.append(Building(**entry))

        del self.j_inv
        # For every building...
        for i, building in enumerate(self.inventory):
            # Update the count lists
            GAME.count_list[i].config(text=display_num(building.count))
            # Update the price lists
            GAME.price_list[i].config(text='$' + display_num(round(building.current_price)))
            # Create a tooltip rollover
            GAME.create_tooltip(building.name, building, i)

        # Recalculate the cps and update the balances
        self.cps_update()
        self.balance += self.cps * (time() - self.pause_time)
        self.earned += self.cps * (time() - self.pause_time)
        self.life_earned += self.cps * (time() - self.pause_time)

        # Updates the cps label
        GAME.cps_show.config(text="Clicks per Second (cps): " + display_num(round(self.cps, 1)))
        print("Finished!")


class Thing:
    def __init__(self, name, current_price, count):
        """
        Parent class for buildings and upgrades
        :param name:
        :param current_price:
        :param count:
        """
        self.count = count
        self.current_price = current_price
        self.name = name


class Upgrade(Thing):
    def __init__(self, name='', effect=0, target='', condition=0, current_price=0, count=0):
        """
        Creates an upgrade object
        :param name:
        :param effect:
        :param target:
        :param condition:
        :param current_price:
        :param count:
        """
        self.effect = effect
        self.target = target
        self.condition = condition
        super().__init__(name, current_price, count)


class Building(Thing):
    def __init__(self, name='', cps=0, current_price=0, count=0, base_price=0):
        """
        Creates a building object
        :param name:
        :param cps:
        :param current_price:
        :param count:
        :param base_price:
        """
        self.cps = cps
        self.base_price = base_price
        super().__init__(name, current_price, count)


if __name__ == '__main__':
    # STARTS THE GAME
    root = tk.Tk()
    PLAYER = Player()
    GAME = GameWindow(root)
    # if there is a saved game...
    if path.exists('CookieClone Save'):
        # import the save
        PLAYER.import_save()
    root.mainloop()

# TODO: Fill out upgrades JSON :(

"""
Notes:
Upgrades:
    --Upgrades will need to be a list of objects that have an effect and a price
    --Buildings will need a multiplier category for these to go into effect
"""