from tkinter import *
import tkinter as tk 
import pandas as pd
import numpy as np

from task import Frequency

def task():
    # Frequency = 47 # Hz
    # Temperature_rise_goal = 30 # degree Celcius
    # Output_power = 250 # watts
    # Efficiency = 95 # %
    # Input_voltage = 115 # volts
    # Ouptut_voltage = 115 # volts
    # Regulation = 5 # in a scale of 100
    # Bobbin_thickness = 1.5 
    # K_f = 4.44
    # K_u = 0.4
    # B_ac = 1.6
    # J = 250

    # insulation_thickness = 0.2 #mm

    Input_voltage = float(Input_Voltage_text.get())
    Output_voltage = float(Output_voltage_text.get())
    Output_power = float(Output_power_text)
    Efficiency = float(Frequency_text.get())
    pass 



"""
UI code below 
"""
app = tk.Tk()
app.title("Auto - Transformer")

input_Voltage_lable = Label(app, text='Input voltage (Vin))')
input_Voltage_lable.grid(row=0, column=0, padx=5, pady=5, sticky=E)

Input_Voltage_text = StringVar()
Input_Voltage_text.set('')
input_Voltage_box = Entry(app, textvariable=Input_Voltage_text)
input_Voltage_box.grid(row=0, column=1, padx=5, pady=5)

output_voltage_lable = Label(app, text='Output voltage [volts]')
output_voltage_lable.grid(row=1, column=0, padx=5, pady=5, sticky=E)

Output_voltage_text = StringVar()
Output_voltage_text.set('')
Output_voltage_box = Entry(app, textvariable=Output_voltage_text)
Output_voltage_box.grid(row=1, column=1, padx=5, pady=5)

Output_power_lable = Label(app, text='Output Power [watts]')
Output_power_lable.grid(row=2, column=0, padx=5, pady=5, sticky=E)

Output_power_text = StringVar()
Output_power_text.set('')
Output_power_box = Entry(app, textvariable=Output_power_text)
Output_power_box.grid(row=2, column=1, padx=5, pady=5)

Efficiency_lable = Label(app, text='Efficiency [100%]')
Efficiency_lable.grid(row=3, column=0, padx=5, pady=5, sticky=E)

Efficiency_text = StringVar()
Efficiency_text.set('')
Efficiency_box = Entry(app, textvariable=Efficiency_text)
Efficiency_box.grid(row=3, column=1, padx=5, pady=5)

Frequency_lable = Label(app, text='Frequency [Hz]')
Frequency_lable.grid(row=4, column=0, padx=5, pady=5, sticky=E)

Frequency_text = StringVar()
Frequency_text.set('')
Frequency_box = Entry(app, textvariable=Frequency_text)
Frequency_box.grid(row=4, column=1, padx=5, pady=5)

app.mainloop()

