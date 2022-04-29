import pandas as pd
import numpy as np
import math 
from decimal import ROUND_DOWN, ROUND_UP


Frequency = 47 # Hz
Temperature_rise_goal = 100 # degree Celcius
Output_power = 250 # watts
Efficiency = 95 # %
Input_voltage = 115 # volts
Ouptut_voltage = 115 # volts
Regulation = 5 # in a scale of 100
Bobbin_thickness = 1.5 
K_f = 4.44
K_u = 0.4
B_ac = 1.6
J = 250
insulation_thickness = 0.2 #mm

pi = np.pi #pi
a = 1.68 # coefficients for core loss
b = 1.86 # coefficients for core loss 

Rate_of_Cu = 950 # Rs / Kg
Rate_of_Fe = 250 # Rs / Kg

Resistivity_Cu =  1.68 * 10**-6 # ohm cm