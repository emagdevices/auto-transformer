# import tkinter as tk
from tkinter import *


class Input_Labels:
    def __init__(self, master):
        self.master = master
        self.master.title("Auto Transformer")

        input_Voltage_lable = Label(master, text='Input voltage (Vin))')
        input_Voltage_lable.grid(row=0, column=0, padx=2, pady=5, sticky=E)

        Input_Voltage_text = StringVar()
        Input_Voltage_text.set('')
        input_Voltage_box = Entry(master, textvariable=Input_Voltage_text)
        input_Voltage_box.grid(row=0, column=1, padx=2, pady=5)

        output_voltage_lable = Label(master, text='Output voltage [volts]')
        output_voltage_lable.grid(row=1, column=0, padx=2, pady=5, sticky=E)

        Output_voltage_text = StringVar()
        Output_voltage_text.set('')
        Output_voltage_box = Entry(master, textvariable=Output_voltage_text)
        Output_voltage_box.grid(row=1, column=1, padx=2, pady=5)

        Output_power_lable = Label(master, text='Output Power [watts]')
        Output_power_lable.grid(row=2, column=0, padx=2, pady=5, sticky=E)

        Output_power_text = StringVar()
        Output_power_text.set('')
        Output_power_box = Entry(master, textvariable=Output_power_text)
        Output_power_box.grid(row=2, column=1, padx=2, pady=5)

        Efficiency_lable = Label(master, text='Efficiency [100%]')
        Efficiency_lable.grid(row=3, column=0, padx=2, pady=5, sticky=E)

        Efficiency_text = StringVar()
        Efficiency_text.set('')
        Efficiency_box = Entry(master, textvariable=Efficiency_text)
        Efficiency_box.grid(row=3, column=1, padx=2, pady=5)

        


root = Tk()
my_gui = Input_Labels(root)
root.mainloop()
