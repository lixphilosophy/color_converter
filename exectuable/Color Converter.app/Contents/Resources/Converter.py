import os
import re
import tkinter as tk


class Converter(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.init_master()
        self.pack()

        self.message_bar = self.init_message_bar()
        self.input_bar = self.init_dialog_frame()

    # custom window configure
    def init_master(self):
        self.master.title("Color Converter")
        self.master.resizable(False, False)
        self.set_geometry(250, 180)
        self.master.tk_setPalette(background="#808080")
        self.master.configure(menu=tk.Menu(self.master))
        self.master.bind("<Return>", self.submit)

    # init function for display window
    def init_message_bar(self):
        message_bar = tk.Canvas(self, height=110, bg="#404040")
        message_bar.pack(fill=tk.X, padx=15, pady=(15, 9))
        return message_bar

    # init function for user input/operate
    def init_dialog_frame(self):
        dialog_frame = tk.Frame(self)
        dialog_frame.pack(fill=tk.X, padx=15)
        dialog_frame.columnconfigure(0, weight=1)
        dialog_frame.columnconfigure(1, weight=1)

        input_bar = tk.Entry(dialog_frame,
                             width=13,
                             bg="#eaeaea",
                             fg="#2d2d2d",
                             font=("Arial", 13),
                             insertbackground="#2d2d2d")
        input_bar.grid(row=0, column=0, sticky=tk.W)

        button = tk.Label(dialog_frame,
                          text="convert",
                          width=9, bg="#4c4c4c",
                          fg="white",
                          font=("Arial", 14, "bold"),
                          takefocus=1)
        button.grid(row=0, column=1, sticky=tk.E, padx=(0, 3))
        button.bind("<Button-1>", self.submit)
        return input_bar

    # output function
    def submit(self, event):
        user_input = self.input_bar.get()
        if user_input:
            print()
            self.input_bar.delete(0, "end")
            self.message_bar.delete("all")

            # check user input format
            regular = re.compile("\d+,\d+,\d+")
            if regular.match(user_input):
                color = user_input.split(",")
                r_value = int(color[0])
                g_value = int(color[1])
                b_value = int(color[2])

                # check input number range
                if color_range_check(r_value, g_value, b_value):
                    self.print_table(r_value, g_value, b_value)
                else:
                    self.message_bar.create_text(110, 50,
                                                 text="Error: Input number out of range",
                                                 font=("Futura", 10),
                                                 fill="white")
            else:
                self.message_bar.create_text(110, 50,
                                             text="Error: Invalid input.",
                                             font=("Futura", 10), fill="white")

    # function for output color information table
    def print_table(self, r_value, g_value, b_value):
        rows = 5
        column_0 = ["RGB(0~255)", "RGB(0~1)", "HEX", "CMYK", "HSL"]
        column_1 = [rgb_to_string(r_value, g_value, b_value),
                    rgb_to_string(r_value, g_value, b_value, if_up=False),
                    rgb_to_hex(r_value, g_value, b_value),
                    rgb_to_cmyk(r_value, g_value, b_value),
                    rgb_to_hsl(r_value, g_value, b_value)]

        table = tk.Frame(self.message_bar, bg="#404040")
        self.message_bar.create_window(110, 60, window=table, width=180, height=80)

        table.columnconfigure(0, weight=1)
        table.columnconfigure(1, weight=1)

        for row in range(rows):
            label1 = tk.Label(table,
                              text=column_0[row],
                              font=("Arial", 9),
                              bg="#404040",
                              fg="white")
            label1.grid(row=row, column=0, sticky=tk.W)
            label2 = tk.Label(table,
                              text=column_1[row],
                              font=("Arial", 9),
                              bg="#404040",
                              fg="white")
            label2.grid(row=row, column=1, sticky=tk.E)

    # function to create geometry coordinate
    def set_geometry(self, width, height):
        x = int(self.master.winfo_screenwidth() * 2/3)
        y = int(self.master.winfo_screenheight() * 3/5)
        self.master.geometry("%dx%d+%d+%d" % (width, height, x, y))


# function input RGB(int, int, int) output boolean
# check if three input in range (0~255)
def color_range_check(r_value, g_value, b_value):
    if 0 <= r_value <= 255 and 0 <= g_value <= 255 and 0 <= b_value <= 255:
        pass
    else:
        return False
    return True


# function input RGB(int, int, int) output RGB(str)
# if_up: False : (0~1) scale, True: (0~255)
def rgb_to_string(r_value, g_value, b_value, if_up=True):
    if if_up:
        return "rgb(" + \
               str(r_value) + ", " + \
               str(g_value) + ", " + \
               str(b_value) + ")"
    return "rgb(" + \
           str(round(r_value / 255, 2)) + ", " + \
           str(round(g_value / 255, 2)) + ", " + \
           str(round(b_value / 255, 2)) + ")"


# function input RGB(int, int, int) output Hex with #ffffff (str)
def rgb_to_hex(r_value, g_value, b_value):
    return "#" + str('%02x%02x%02x' % (r_value, g_value, b_value))


# function input RGB(int, int, int) output cmyk (str)
def rgb_to_cmyk(r_value, g_value, b_value):
    c_value = float(1 - r_value / 255)
    m_value = float(1 - g_value / 255)
    y_value = float(1 - b_value / 255)

    min_cmy = min(c_value, m_value, y_value)

    c_value = int(((c_value - min_cmy) / (1 - min_cmy)) * 100)
    m_value = int(((m_value - min_cmy) / (1 - min_cmy)) * 100)
    y_value = int(((y_value - min_cmy) / (1 - min_cmy)) * 100)
    k_value = int(min_cmy * 100)

    return "cmyk(" + \
           str(c_value) + "%, " + \
           str(m_value) + "%, " + \
           str(y_value) + "%, " + \
           str(k_value) + "%)"


# function input RGB(int, int, int) output hsl (str)
def rgb_to_hsl(r_value, g_value, b_value):
    r_value = r_value / 255
    g_value = g_value / 255
    b_value = b_value / 255

    max_value = max(r_value, g_value, b_value)
    min_value = min(r_value, g_value, b_value)

    l_value = (max_value + min_value) / 2

    if max_value == min_value:
        h_value = s_value = 0
    else:
        diff = max_value - min_value
        if l_value > 0.5:
            s_value = diff / (2 - max_value - min_value)
        else:
            s_value = diff / (max_value + min_value)

        if max_value == r_value:
            h_value = (g_value - b_value) / diff
        elif max_value == g_value:
            h_value = (b_value - r_value) / diff + 2
        else:
            h_value = (r_value - g_value) / diff + 4

        h_value = h_value * 60
        if h_value < 0:
            h_value = h_value + 360

    h_value = int(round(h_value))
    s_value = int(round(s_value, 2) * 100)
    l_value = int(round(l_value, 2) * 100)

    return "hsl(" + \
           str(h_value) + ", " + \
           str(s_value) + "%, " + \
           str(l_value) + "%)"


if __name__ == '__main__':
    root = tk.Tk()
    converter = Converter(root)
    root.mainloop()
