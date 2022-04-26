# Loading libraries
import pandas as pd
import numpy as np
import math 
from decimal import ROUND_DOWN, ROUND_UP
from strip_function import *


# Initial variables for the calculation and validation
Frequency = 47 # Hz
Temperature_rise_goal = 30 # degree Celcius
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

# Loadin Data
# lamination_data = pd.read_csv('../DATA/EI-Laminations.csv')
lamination_data = data.lamination_data
# swg_data = pd.read_csv('../DATA/EMD - Sheet1.csv') # select the swg the data 
swg_data = data.swg_data

# Calculate Apparent power
Apparent_power = Output_power * (1/(0.01*Efficiency) + 1)
# Calculate Area product
Area_product = area_product(K_f, K_u, B_ac, J, Frequency, Apparent_power)

Input_current = Apparent_power / (Input_voltage * 0.01*  Efficiency)
A_wp_in_sqmm = bare_area(Input_current, J)
required_swg_primary, diameter_of_primary_wire_with_insulation, A_wp = findSWG(A_wp_in_sqmm)

print('Input current ' + str(Input_current) + ' [amps]')
print('Calculated Priamry Bare Area: ' + str(A_wp_in_sqmm)+ ' mm²')
print('Final Priamry Bare Area after selecting swg: ' + str(A_wp*100)+ ' mm²')
print('SWG: ' + str(required_swg_primary['SWG'].to_string(index=False)))
print('Primary wire Diameter with enamel: ' + str(diameter_of_primary_wire_with_insulation.max()) + ' mm')