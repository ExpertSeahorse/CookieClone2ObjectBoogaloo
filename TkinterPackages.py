import tkinter as tk


class CreateToolTip(object):
    # I didn't create this class and therefore only understand how to use it
    """
    tk_ToolTip_class101.py
    gives a Tkinter widget a tooltip as the mouse is above the widget
    tested with Python27 and Python34  by  vegaseat  09sep2014
    www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter

    Modified to include a delay time by Victor Zaccardo, 25mar16
    """

    def __init__(self, widget, text='widget info'):
        """
        Binds a tooltip with the provided text to the provided widget
        :param widget:
        :param text:
        """
        self.wait_time = 100  # milliseconds
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
