import tkinter as tk
import json
from time import time
import re
# TODO: Add "buy 10x & 100x"
# TODO: Add upgrades
# TODO: Add Mouse over menu for each building's: cps, %of total, total cookies so far
# TODO: Add Stats rollover page
# TODO: Add restarting incentive (Ascend)


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
        self.shoptitlelist = ["price", "building", "quantity"]
        for i, entry in enumerate(self.shoptitlelist):
            self.entry = tk.Label(self.frame_shop, text=entry.capitalize())
            self.entry.grid(row=1, column=i)

        # Creates the entire shop: Prices, Buy buttons, & Quantity numbers based on PLAYER.inventory
        self.count_list = []
        self.price_list = []
        index = 1
        r = 2
        for key in PLAYER.inventory:
            label = key.lower().capitalize()

            # makes price labels
            self.price_name = tk.Label(self.frame_shop, width=20,
                                       text='$' + str(GameWindow.display_num(PLAYER.inventory[key][2])))
            self.price_name.grid(row=r)
            self.price_list.append(self.price_name)

            # makes purchase buttons
            self.but_name = tk.Button(self.frame_shop, text=label, width=20, command=lambda j=index: self.buy(j))
            self.but_name.grid(row=r, column=1)

            # makes count labels
            self.key = tk.Label(self.frame_shop, width=20, text=str(PLAYER.inventory[key][0]))
            self.key.grid(row=r, column=2)
            self.count_list.append(self.key)
            r += 1
            index += 1

        self.export_button = tk.Button(master, width=10, text="Export Save", command=PLAYER.export_save)
        self.export_button.pack()

        self.import_button = tk.Button(master, width=10, text="Import Save", command=PLAYER.import_save)
        self.import_button.pack()

    def ck_click(self):
        """
        If the player clicks the cookie, add a cookie and update the balance
        :return:
        """
        PLAYER.balance += 1
        self.bal_show.config(text="Balance: " + str(GameWindow.display_num(round(PLAYER.balance))))

    def buy(self, choice):
        """
        Runs the backend for purchasing buildings
        :param choice:
        :return:
        """
        index = 1
        # For every building possible...
        for key in PLAYER.inventory:
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
                    self.bal_show.config(text="Balance: " + str(GameWindow.display_num(round(PLAYER.balance))))
                    # Update the building's count list
                    self.count_list[choice - 1].config(text=GameWindow.display_num(PLAYER.inventory[key][0]))
                    # Update the building's price list
                    self.price_list[choice - 1].config(text='$' +
                                                       str(GameWindow.display_num(round(PLAYER.inventory[key][2]))))
                    # Recalculate and update the cps
                    PLAYER.cps_update()
                    self.cps_show.config(text="Clicks per Second (cps): " + str(GameWindow.display_num(PLAYER.cps)))
                    break
            index += 1

    def game_tick(self):
        """
        Adds the amount of cookies the player should receive every second
        :return:
        """
        # Ensure the cps is correct
        PLAYER.cps_update(game_tick=1)
        # Add the cps to the player's balance
        PLAYER.balance += PLAYER.cps
        # Update the balance
        self.bal_show.config(text="Balance: " + str(GameWindow.display_num(round(PLAYER.balance))))
        self.save_counter += 1
        if self.save_counter % 30000 == 0:
            self.save_counter = 0
            PLAYER.export_save()
        # Repeat after 1000ms
        self.bal_show.after(10, self.game_tick)

    @staticmethod
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
            return num

    class HoverInfo(tk.Menu):
        # TODO: Get this hover over menu working
        # https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python/20399283
        def __init__(self, parent, text, command=None):
            self._com = command
            tk.Menu.__init__(self, parent, tearoff=0)
            if not isinstance(text, str):
                raise TypeError('Trying to initialise a Hover Menu with a non string type: ' + text.__class__.__name__)
            toktext = re.split('\n', text)
            for t in toktext:
                self.add_command(label=t)
            self._displayed = False
            self.master.bind("<Enter>", self.display)
            self.master.bind("<Leave>", self.remove)

        def __del__(self):
            self.master.unbind("<Enter>")
            self.master.unbind("<Leave>")

        def display(self, event):
            if not self._displayed:
                self._displayed = True
                self.post(event.x_root, event.y_root)
            if self._com:
                self.master.unbind_all("<Return>")
                self.master.bind_all("<Return>", self.click)

        def remove(self, event):
            if self._displayed:
                self._displayed = False
                self.unpost()
            if self._com:
                self.unbind_all("<Return>")

        def click(self, event):
            self._com()


########################################################################################################################


class Player:
    def __init__(self):
        self.balance = 0
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
        self.cps = 0
        self.start_time = time()
        self.full_inventory = {}

    def cps_update(self, game_tick=0):
        """
        Updates the player's cps based on inventory
        :return:
        """
        self.cps = 0
        for key, value in self.inventory.items():
            if not game_tick:
                self.cps += value[0] * value[1]
            elif game_tick == 1:
                self.cps += value[0] * (value[1]/100)

    def export_save(self):
        print("Starting save...")
        self.full_inventory = {'balance': self.balance,
                               'inventory': self.inventory,
                               'time': self.start_time}
        with open("CookieClone Save", "w", encoding="utf-8") as file:
            json.dump(self.full_inventory, file, ensure_ascii=False, indent=2)
        print("Finished!")

    def import_save(self):
        print("Loading save...")
        with open("CookieClone Save", "r", encoding="utf-8") as file:
            self.full_inventory = json.load(file)
        self.balance = self.full_inventory['balance']
        self.inventory = self.full_inventory['inventory']
        self.start_time = self.full_inventory['time']
        # self.time = self.full_inventory['time']

        i = 0
        for key in self.inventory:
            # Update all building count lists
            GAME.count_list[i].config(text=GameWindow.display_num(self.inventory[key][0]))
            # Update all building price lists
            GAME.price_list[i].config(text='$' +
                                           str(GameWindow.display_num(round(self.inventory[key][2]))))
            i += 1

        # Recalculate and update the cps
        self.cps_update()
        self.balance += self.cps * (time() - self.start_time)
        GAME.cps_show.config(text="Clicks per Second (cps): " + str(GameWindow.display_num(round(self.cps, 1))))

        print("Finished!")


if __name__ == '__main__':
    # STARTS THE GAME
    PLAYER = Player()
    root = tk.Tk()
    GAME = GameWindow(root)
    root.mainloop()
