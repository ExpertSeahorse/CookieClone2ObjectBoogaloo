import tkinter as tk
import json
from time import time
from os import path
# TODO: Add "buy 10x & 100x"
# TODO: Add upgrades
# TODO: Add restarting incentive (Ascend)
# TODO: Add scrollbar for smaller screens
# TODO: Achievements


class GameWindow:
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

        # Creates the entire shop: Prices, Buy buttons, & Quantity numbers based on PLAYER.inventory
        self.count_list = []
        self.price_list = []
        self.button_lst = []
        index = 1
        r = 2
        for key, entry in PLAYER.inventory.items():
            label = key.lower().capitalize()

            # makes price labels
            self.price_name = tk.Label(self.frame_shop, width=21,
                                       text='$' + display_num(entry[2]))
            self.price_name.grid(row=r)
            self.price_list.append(self.price_name)

            # makes purchase buttons
            self.but_name = tk.Button(self.frame_shop, text=label, width=20, command=lambda j=index: self.buy(j))
            self.but_name.grid(row=r, column=1)
            self.button_lst.append(self.but_name)

            self.create_tooltip(key, entry, index - 1)

            # makes count labels
            self.key = tk.Label(self.frame_shop, width=21, text=str(PLAYER.inventory[key][0]))
            self.key.grid(row=r, column=2)
            self.count_list.append(self.key)

            r += 1
            index += 1
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

    def create_tooltip(self, key, entry, index):
        """
        Creates tooltips
        :param key:
        :param entry:
        :param index:
        :return:
        """
        label = key.capitalize()
        # Gets the cps created by the building type
        build_cps = entry[0] * entry[1]
        PLAYER.cps_update()
        # Gets the % of the cps contributed by the building type
        try:
            build_cps_ratio = str(round(build_cps / PLAYER.cps * 100, 1))
        except ZeroDivisionError:
            build_cps_ratio = str(0.0)

        # Creates the tooltip
        CreateToolTip(self.button_lst[index],
                           "--Each " + label + " produces " + display_num(entry[1]) + " cookies per second\n" +
                           "--" + display_num(entry[0]) + " " + label + "s producing " + display_num(build_cps) + " cookies per second (" + build_cps_ratio + "%)")

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
        index = 1
        # For every building possible...
        for key, building in PLAYER.inventory.items():
            # If the player bought one of these buildings...
            if choice == index:
                # And if the player can afford it at it's current price...
                if PLAYER.balance >= PLAYER.inventory[key][2]:
                    # Take the cookies from the player
                    PLAYER.balance -= PLAYER.inventory[key][2]
                    # Give the player one building
                    PLAYER.inventory[key][0] += 1
                    # Raise the price of the next building
                    PLAYER.inventory[key][2] *= 1.15

                    # Update their balance
                    self.bal_show.config(text="Balance: " + display_num(round(PLAYER.balance)))
                    # Update the building's count list
                    self.count_list[choice - 1].config(text=display_num(building[0]))
                    # Update the building's price list
                    self.price_list[choice - 1].config(text='$' +
                                                       display_num(round(building[2])))
                    # Recalculate and update the cps
                    PLAYER.cps_update()
                    self.cps_show.config(text="Clicks per Second (cps): " + display_num(PLAYER.cps))

                    # Update all the tooltips (for cps%)
                    i = 0
                    for name, entry in PLAYER.inventory.items():
                        self.create_tooltip(name, entry, i)
                        i += 1
                    break
            index += 1

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



    # noinspection PyAttributeOutsideInit
    def stats_win(self):
        self.app = self.Stats(tk.Toplevel(self.master))



    class Stats:
        def __init__(self, master):
            PLAYER.stats = {'balance': display_num(round(PLAYER.balance)),
                            'earned': display_num(round(PLAYER.earned)),
                            'lifetime': display_num(round(PLAYER.life_earned)),
                            'cps': display_num(round(PLAYER.cps * 100)),
                            'init_time': PLAYER.start_time,
                            'building count': PLAYER.building_counter(),
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


class Player:
    def __init__(self):
        # Stores the balance in the bank
        self.balance = 0
        # Stores the balance earned this run
        self.earned = 0
        # Stores the lifetime balance (Ascend needed)
        self.life_earned = 0
        # Stores the buildings, their count, their cps, and their price
        self.inventory = {'auto clicker': [0, .1, 10],
                          'grandma': [0, 1, 100],
                          'farm': [0, 8, 1100],
                          'mine': [0, 47, 12000],
                          'factory': [0, 260, 130000],
                          'bank': [0, 1400, 1.4*10**6],
                          'temple': [0, 7800, 2*10**7],
                          'wizard tower': [0, 44000, 3.3*10**8],
                          'shipment': [0, 260000, 5.1*10**9],
                          'alchemy lab': [0, 1.6*10**6, 7.5*10**10],
                          'portal': [0, 1*10**7, 1*10**12],
                          'time machine': [0, 6.5*10**7, 1.4*10**13],
                          'anti-matter condenser': [0, 4.3*10**8, 1.7*10**14],
                          'prism': [0, 2.9*10**9, 2.1*10**15],
                          'chance maker': [0, 2.1*10**10, 2.6*10**16],
                          'fractal engine': [0, 1.5*10**11, 3.1*10**17]}
        #                 'key_name': [count, cps, price]

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
        for key, value in self.inventory.items():
            # If the calculation isn't for the game logic...
            if not game_tick:
                # the cps is the sum of the number of buildings multiplied by their cps value
                self.cps += value[0] * value[1]
            # if the calculation is for the actual game logic...
            elif game_tick == 1:
                # the cps of each building is 1/100 the advertised value b/c the game tick happens every 1/100 seconds
                self.cps += value[0] * (value[1]/100)

    def building_counter(self):
        """
        Counts the total number of buildings for the stats dict
        :return:
        """
        total = 0
        for key in self.inventory:
            total += self.inventory[key][0]
        return total

    def export_save(self):
        """
        Creates a save file with all of the information needed to reload the game
        :return:
        """
        print("Starting save...")
        # Sets the pause time
        # The program will use this time to calculate the time passed for the sleep cookies to e calculated
        self.pause_time = time()
        # Loads the stats dict to commit to the save
        # Stores the entire dict even though we don't need it to maintain the structure for the stats page
        self.stats = {'balance': self.balance,
                      'earned': self.earned,
                      'lifetime': self.life_earned,
                      'cps': self.cps_update(),
                      'init_time': self.start_time,
                      'pause_time': time(),
                      'building count': self.building_counter(),
                      'click_str': self.click_str,
                      'handmade': self.handmade,
                      'inventory': self.inventory}
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
        self.inventory = self.stats['inventory']

        i = 0
        # For every building...
        for key, building in self.inventory.items():
            # Update the count lists
            GAME.count_list[i].config(text=display_num(building[0]))
            # Update the price lists
            GAME.price_list[i].config(text='$' + display_num(round(building[2])))
            # Create a tooltip rollover
            GAME.create_tooltip(key, building, i)

            i += 1

        # Recalculate the cps and update the balances
        self.cps_update()
        self.balance += self.cps * (time() - self.pause_time)
        self.earned += self.cps * (time() - self.pause_time)
        self.life_earned += self.cps * (time() - self.pause_time)

        # Updates the cps label
        GAME.cps_show.config(text="Clicks per Second (cps): " + display_num(round(self.cps, 1)))
        print("Finished!")


# I didn't create this class and therefore have only a working knowledge of how it works
# noinspection PyUnusedLocal,PyAttributeOutsideInit
class CreateToolTip(object):
    """
    tk_ToolTip_class101.py
    gives a Tkinter widget a tooltip as the mouse is above the widget
    tested with Python27 and Python34  by  vegaseat  09sep2014
    www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter

    Modified to include a delay time by Victor Zaccardo, 25mar16
    """

    def __init__(self, widget, text='widget info'):
        self.wait_time = 300  # milliseconds
        self.wrap_length = 400  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id_ = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id_ = self.widget.after(self.wait_time, self.showtip)

    def unschedule(self):
        id_ = self.id_
        self.id_ = None
        if id_:
            self.widget.after_cancel(id_)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        self.label = tk.Label(self.tw, text=self.text, justify='left',
                              background="#ffffff", relief='solid', borderwidth=1,
                              wraplength=self.wrap_length)
        self.label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


def time_delta_display(sec):
        # Conversion key
        intervals = (('weeks', 604800),  # 60 * 60 * 24 * 7
                     ('days', 86400),    # 60 * 60 * 24
                     ('hours', 3600),    # 60 * 60
                     ('minutes', 60),
                     ('seconds', 1),)
        result = []
        # For each of the above categories...
        for name, count in intervals:
            # Divide the input number of seconds by the counter from the list
            value = sec // count
            # If that value is > 0...
            if value:
                # Subtract the whole number amount from the inputted number(we use the remainder in later iterations)
                sec -= value * count
                # If there is only 1 instance of the unit (1 week, 1 hour, ...)...
                if value == 1:
                    # Remove the 's' from the displayed name
                    name = name.rstrip('s')
                # Add the unit and amount to an array
                result.append("{} {}".format(value, name))
        # Return the array as a string
        return ', '.join(result)

def display_num(num):
        """
        Formats the numbers to include numbers after 1,000,000
        :param num:
        :return:
        """
        if 1 <= num / (1*10**6) < 1000:
            return str(round(num/(1*10**6), 2)) + " million"

        elif 1 <= num / (1*10**9) < 1000:
            return str(round(num/(1*10**9), 2)) + " billion"

        elif 1 <= num / (1*10**12) < 1000:
            return str(round(num/(1*10**12), 2)) + " trillion"

        elif 1 <= num / (1*10**15) < 1000:
            return str(round(num/(1*10**15), 2)) + " quadrillion"

        else:
            return str(num)

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

"""
Notes:
Upgrades:
    --Upgrades will need to be a list of objects that have an effect and a price
    --Buildings will need a multiplier category for these to go into effect
Multi-Purchases:
    --Use 3 radio buttons that all fit into one grid cell, formatted to look like real buttons
    --Import their value into the buy to determine amount purchased
"""