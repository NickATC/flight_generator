import tkinter as tk
from tkinter import Menu
from tkinter import messagebox as msg
from tkinter import ttk
from tkinter import scrolledtext


class GuiMaker():
    """Class to create widgtes easily"""

    def create_label(self, frame, widget_name, text, x_val, y_val):
        """module to create a standard ttk Label"""
        widget_name = ttk.Label(frame, text=text)
        widget_name.place(x=x_val, y=y_val)

    def create_button(self, frame, widget_name, text, width, command, x_val, y_val):
        """module to create a standard ttk Button"""
        widget_name = ttk.Button(
            frame, text=text, width=width, command=command)
        widget_name.place(x=x_val, y=y_val)

    def create_red_button(self, frame, widget_name, text, width, command, x_val, y_val):
        """module to create a RED ttk Button...
        usually for important actions in the GUI"""
        widget_name = tk.Button(frame, text=text, width=width,
                                height=2, font=("30"), command=command,
                                foreground="white", background='red')
        widget_name.place(x=x_val, y=y_val)
