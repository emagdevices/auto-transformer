# %%
import pandas as pd
import numpy as np
import math

# %%
from autotransformer import *
spt = AutoTransformer()

# %%
# Inputs for the function
frequency = 50  # Hz
temperature_rise_goal = 200  # celcius
output_power = 800  # watts
input_voltage = 230 # volts
output_voltage = 230  # volts
efficiency = 99  # %
regulation = 5
b_ac = 1.35  # flux density
current_density = 300  # amp/cm2
Core_Loss_Factor = 1.5 
bobbin_thickness = 1.5  # mm
insulation_thickness = 0.2  # mm
Resistivity_conductor = 1.68 * 10**-6 # ohm cm

# %%
# from auto transformer
k_f = spt.k_f
k_u = spt.k_u
lamination_data = spt.lamination_data
swg_data = spt.swg_data
strip_data = spt.strip_data

# %%
print(spt.core_loss_factor(frequency, b_ac)) 

# %%
strip_data

# %%
# calculate the apparent power
apparent_power = spt.apparent_power(output_power, efficiency)
apparent_power

# %%
# area product
area_product = spt.area_product(apparent_power,b_ac, current_density,frequency, k_f, k_u)
area_product = area_product * 10**4
area_product

# %%
##############################################################
#                       Primary wire
# calculate the input current
input_current = output_power / input_voltage
# bare area in mm2
a_wp = spt.bare_area(input_current, current_density)
# for primary wire
required_strip_primary, actual_a_wp, height_priamry, width_primary = spt.find_strip_lamination(a_wp)

# d_wp = diameter_of_primary_wire
print(input_current)
print(height_priamry)
print(required_strip_primary)

# %%
##############################################################
#                     Secondary Wire
# calculate secondary current
secondary_current = output_power / output_voltage
# bare area secondary in mm2
a_ws = spt.bare_area(secondary_current, current_density)
# for secondary wire
# required_swg_secondary, diameter_of_secondary_wire, actual_a_ws = spt.find_swg(a_ws)

required_strip_secondary, actual_a_ws, height_secondary, width_secondary = spt.find_strip_lamination(a_ws)

# %%
# %%
def strip_cost(stack, tongue, winding_width, winding_lenghth):
    
    if stack < 5 * tongue:

        A_c = spt.core_area(stack, tongue)

        # ************************ Primary Wire ******************************** 

        Number_of_primary_turns = spt.primary_turns(input_voltage, b_ac, frequency, A_c)

        Number_of_primary_turns = round(Number_of_primary_turns)

        Turns_per_layer_primary = math.floor(spt.turns_per_layer_strip(winding_lenghth, width_primary))

        Number_of_layers_primary = math.ceil(spt.number_of_layers(Number_of_primary_turns, Turns_per_layer_primary))

        Built_primary = spt.built_primary_strip(Number_of_layers_primary, height_priamry, insulation_thickness)

        MTL_primary = spt.mtl_primary(tongue, stack, bobbin_thickness, Built_primary)

        Length_primary = spt.length(MTL_primary, Number_of_primary_turns)

        Primary_resistance = spt.resistance(Resistivity_conductor, Length_primary, actual_a_wp)

        Primary_copper_loss = spt.conductor_loss(input_current, Primary_resistance)

        # ************************ Primary Wire ******************************** 

        # ************************ Secondary Wire ******************************

        Number_of_secondary_turns = spt.secondary_turns(Number_of_primary_turns, output_voltage, regulation, input_voltage)

        Number_of_secondary_turns = round(Number_of_secondary_turns)

        Turns_per_layer_secondary = math.floor(spt.turns_per_layer_strip(winding_lenghth, width_secondary))

        Number_of_layers_secondary = math.ceil(spt.number_of_layers(Number_of_secondary_turns, Turns_per_layer_secondary))

        Built_secondary = spt.built_secondary_strip(Number_of_layers_secondary, height_secondary, insulation_thickness)

        MTL_secondary = spt.mtl_secondary(tongue, stack, Built_primary, Built_secondary, bobbin_thickness)

        Length_secondary = spt.length(MTL_secondary, Number_of_secondary_turns)

        Secondary_resistance = spt.resistance(Resistivity_conductor, Length_secondary, actual_a_ws)

        Secondary_copper_loss = spt.conductor_loss(secondary_current, Secondary_resistance)

        # ************************ Secondary Wire ******************************

        Weight_of_copper_kg = (Length_primary * required_strip_primary['Conductor Weight for 1000m/Kg'].max() + Length_secondary * required_strip_secondary['Conductor Weight for 1000m/Kg'].max() ) / 10**5  #kg

        Total_Built = spt.total_built(Built_primary, Built_secondary, bobbin_thickness)

        if winding_width * 0.9 > Total_Built:

            Total_Cu_loss = spt.total_copper_loss(Primary_copper_loss, Secondary_copper_loss)

            # Core_loss_factor = spt.core_loss_factor(frequency, b_ac) 
            Core_loss_factor = Core_Loss_Factor

            volume_of_core = spt.volume_of_core(stack, tongue, winding_width, winding_lenghth)

            Density_of_core = 7.65 # g/cm^3

            weight_of_core = spt.weight_of_core(Density_of_core, volume_of_core)

            weight_of_core_kg = weight_of_core / 1000  # kg

            core_loss = spt.core_loss(Core_loss_factor, weight_of_core_kg) 

            total_loss = spt.total_loss(Total_Cu_loss, core_loss)

            conductor_surface_area = spt.conductor_surface_area(stack, Total_Built, tongue, winding_lenghth)  # cm2

            core_surface_area = spt.core_surface_area(stack, tongue, winding_lenghth, winding_width)  # cm2

            total_surface_area = spt.total_surface_area(stack, tongue, winding_lenghth, winding_width, Total_Built)  # cm2

            psi_copper = spt.psi(Total_Cu_loss, conductor_surface_area)

            temperature_rise_copper = spt.temperature_rise(psi_copper)

            psi_core = spt.psi(core_loss, core_surface_area)

            temperature_rise_core = spt.temperature_rise(psi_core)

            cost = spt.cost(weight_of_core_kg, Weight_of_copper_kg, rate_copper=950, rate_fe=160)

            results_data = {
                    'Stack mm': stack,
                    'Tongue mm': tongue,
                    'Winding width mm': winding_width,
                    'Winding lenght mm': winding_lenghth,
                    'Length primary': Length_primary,
                    'Length secondary': Length_secondary,
                    'Cu surface area': conductor_surface_area,
                    'Core surface area': core_surface_area,
                    'Weight of Fe': weight_of_core_kg,
                    'Weight of Cu kg': Weight_of_copper_kg,
                    'Cu Temperature rise': temperature_rise_copper,
                    'Fe Temperature rise': temperature_rise_core,
                    'Cost': cost
                }

            return results_data 

# %%
strip_data_result= []

"""
write down the strip algorithm under this cell

Area = s * t * ww * wl

s, t, ww, wl muliples of 5

s * t * ww * wl  <= Area_product

95 < stack < 400
120 < t < 250
20 < ww < 250
120 < wl < 600

s = [50, 55, 60 ... 445]
t = [50, 55, .. ]

example stack_cost(50, 200, 600, 50)
"""
for stack in range(95, 400, 5):
    for tongue in range(120, 250, 5):
        if stack < 3 * tongue and stack > 0.8 * tongue:
            for ww in range(20, 250, 5):
                for wl in range(120, 600, 5):
                    product = stack * tongue * ww * wl 
                    if area_product * 1.5 > product and area_product * 0.5 < product:
                        results = strip_cost(stack, tongue, ww, wl)
                        if results:
                            strip_data_result.append(results)

final_result = pd.DataFrame(strip_data_result)

# %%
final_result
print(final_result) 

# %%
if final_result.empty:
    print(final_result)
else:
    print(final_result.sort_values('Cost'))


