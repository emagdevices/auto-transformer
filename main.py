# Load libraries
import pandas as pd
import numpy as np

# Inputs and constants 
Frequency = 47 # Hz
Temperature_rise_goal = 30 # degree Celcius
Output_power = 250 # watts
Ouptut_voltage = 115 # volts
Efficiency = 95 # %
Input_voltage = 115 # volts
Bobbin_thickness = 1.5 
Regulation = 5 # percent
K_f = 4.44
K_u = 0.4
B_ac = 1.6
J = 250 # amps / cm^2


Apparent_power = Output_power * (1/(0.01*Efficiency) + 1)
print('Apparent power: ' + str(Apparent_power) + ' watts')


Area_product = (Apparent_power*(10**4))/(K_f * K_u * B_ac * J * Frequency)
print('Theoretical Area product: ' + str(Area_product) + ' cm^4') 


# import lamination data
lamination_data = pd.read_csv('./EI-Laminations - Sheet1.csv')
# import swg data 
swg_data = pd.read_csv('EMD - Sheet1.csv')


""" Inpu Current
    Primary Bare Wire Area 
    Diameter of Primary Bare Wire with Insulation 
"""
# Input current I_input
# Input_current = Apparent_power / (Input_voltage*Efficiency)
Input_current = Apparent_power / (Input_voltage * 0.01* Efficiency)
print('Input current ' + str(Input_current) + ' [amps]')

# Primary bare wire area A_wp
# A_wp = Input_current / Current_density (J)
A_wp = Input_current / J
print('Priamry Bare Area: ' + str(A_wp*100)+ ' mm^2') # bare area in sqcm so convert it into sqmm

A_wp_in_sqmm = A_wp * 100

# swg_data = pd.read_csv('EMD - Sheet1.csv')
required_swg_primary = swg_data.iloc[(swg_data['Normal Conductor Area mm²'] - A_wp_in_sqmm).abs().argsort()[:1]]
print('SWG: ' + str(required_swg_primary['SWG'].to_string(index=False)))

# Diameter of primary wire with insulation enamel
diameter_of_primary_wire_with_insulation = required_swg_primary['Medium Covering Max']
print('Primary wire Diameter with enamel: ' + str(diameter_of_primary_wire_with_insulation.max()) + ' mm')