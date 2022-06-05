# %%
import pandas as pd
import numpy as np
import math

# %%
from autotransformer import *
spt = AutoTransformer()

# %%
# Inputs for the function
frequency = 47  # Hz
temperature_rise_goal = 200  # celcius
output_power = 1000  # watts
input_voltage = 230  # volts
output_voltage = 230  # volts
efficiency = 95  # %
regulation = 5
b_ac = 1.45  # flux density
current_density = 300  # amp/cm2
bobbin_thickness = 1.5  # mm
insulation_thickness = 0.2  # mm
Resistivity_conductor = 1.68 * 10**-6 # ohm cm

# core loss factor as new input variable
Core_Loss_Factor = 1.5 

# %%
# from auto transformer
k_f = spt.k_f
k_u = spt.k_u
lamination_data = spt.lamination_data
swg_data = pd.read_csv('https://raw.githubusercontent.com/emagdevices/auto-transformer/main/DATA/Wires_data.csv')


# %%
swg_data

# %%
# calculate the apparent power
apparent_power = spt.apparent_power(output_power, efficiency)
apparent_power

# %%
# area product
area_product = spt.area_product(apparent_power,b_ac, current_density,frequency, k_f, k_u)
area_product

# %%
##############################################################
#                       Primary wire
# calculate the input current
input_current = output_power / input_voltage
# bare area in mm2
a_wp = spt.bare_area(input_current, current_density)
# for primary wire
# required_swg_primary, diameter_of_primary_wire, actual_a_wp = spt.find_swg(a_wp)
required_strip_primary, actual_a_wp, height_priamry, width_primary = spt.find_strip_lamination(a_wp)
# d_wp = diameter_of_primary_wire

print(input_current)
print(height_priamry)
print(a_wp)
print(required_strip_primary)
#                       Primary wire
##############################################################

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
# d_ws = diameter_of_secondary_wire
print(a_ws)
print(actual_a_ws)
#                     Secondary Wire
##############################################################

# %%
stack_data = []

for lamination in lamination_data['Type']:

    selected_lamination = lamination_data[lamination_data['Type'] == lamination]

    for x in range(60, 141, 5):

        tongue = selected_lamination['Tongue'].max()  # mm

        wl = selected_lamination['Winding-length'].max() # mm
        
        ww = selected_lamination['Winding-width'].max() # mm 

        present_area_product = x * 0.01 * area_product

        stack = spt.calculate_stack(present_area_product, selected_lamination['K-ratio'].max())

        if stack < 5 * tongue:

            stack = spt.rounding_stack_as_multiple_of_five(stack)  # mm 

            A_c = spt.core_area(stack, tongue)  # cm2

            # ************************ Primary Wire ******************************** 

            Number_of_primary_turns = spt.primary_turns(input_voltage, b_ac, frequency, A_c)

            Number_of_primary_turns = round(Number_of_primary_turns)

            Turns_per_layer_primary = math.floor(spt.turns_per_layer(wl, width_primary))

            Number_of_layers_primary = math.ceil(spt.number_of_layers(Number_of_primary_turns, Turns_per_layer_primary))

            Built_primary = spt.built_primary(Number_of_layers_primary, height_priamry, bobbin_thickness)

            MTL_primary = spt.mtl_primary(tongue, stack, bobbin_thickness, Built_primary)

            Length_primary = spt.length(MTL_primary, Number_of_primary_turns)

            Primary_resistance = spt.resistance(Resistivity_conductor, Length_primary, actual_a_wp)

            Primary_copper_loss = spt.conductor_loss(input_current, Primary_resistance)

            # ************************ Primary Wire ******************************** 

            # ************************ Secondary Wire ******************************

            Number_of_secondary_turns = spt.secondary_turns(Number_of_primary_turns, output_voltage, regulation, input_voltage)

            Number_of_secondary_turns = round(Number_of_secondary_turns)

            Turns_per_layer_secondary = math.floor(spt.turns_per_layer(wl, width_secondary))

            Number_of_layers_secondary = math.ceil(spt.number_of_layers(Number_of_secondary_turns, Turns_per_layer_secondary))

            Built_secondary = spt.built_secondary(Number_of_layers_secondary, height_secondary, insulation_thickness)

            MTL_secondary = spt.mtl_secondary(tongue, stack, Built_primary, Built_secondary, bobbin_thickness)

            Length_secondary = spt.length(MTL_secondary, Number_of_secondary_turns)

            Secondary_resistance = spt.resistance(Resistivity_conductor, Length_secondary, actual_a_ws)

            Secondary_copper_loss = spt.conductor_loss(secondary_current, Secondary_resistance)

            # ************************ Secondary Wire ******************************

            Weight_of_copper_kg = (Length_primary * required_strip_primary['Conductor Weight for 1000m/Kg'].max() + Length_secondary * required_strip_secondary['Conductor Weight for 1000m/Kg'].max() ) / 10**5  #kg

            Total_Built = spt.total_built(Built_primary, Built_secondary, bobbin_thickness)

            if (ww * 0.9 > Total_Built):

                Total_Cu_loss = spt.total_copper_loss(Primary_copper_loss, Secondary_copper_loss)

                Core_loss_factor = spt.core_loss_factor(frequency, b_ac) 

                volume_of_core = spt.volume_of_core(stack, tongue, ww, wl)

                Density_of_core = 7.65 # g/cm^3

                weight_of_core = spt.weight_of_core(Density_of_core, volume_of_core)

                weight_of_core_kg = weight_of_core / 1000  # kg

                core_loss = spt.core_loss(Core_loss_factor, weight_of_core_kg) 

                total_loss = spt.total_loss(Total_Cu_loss, core_loss)

                conductor_surface_area = spt.conductor_surface_area(stack, Total_Built, tongue, wl)  # cm2

                core_surface_area = spt.core_surface_area(stack, tongue, wl, ww)  # cm2

                total_surface_area = spt.total_surface_area(stack, tongue, wl, ww, Total_Built)  # cm2

                psi_copper = spt.psi(Total_Cu_loss, conductor_surface_area)

                temperature_rise_copper = spt.temperature_rise(psi_copper)

                psi_core = spt.psi(core_loss, core_surface_area)

                temperature_rise_core = spt.temperature_rise(psi_core)

                cost = spt.cost(weight_of_core_kg, Weight_of_copper_kg, rate_copper=950, rate_fe=250)

                if (temperature_rise_copper < temperature_rise_goal) and (temperature_rise_core < temperature_rise_goal):
                    results_data = {
                        'x %': x,
                        'Lamination': selected_lamination['Type'].max(),
                        'Area product': present_area_product,
                        'Stack mm': stack,
                        'Tongue mm': tongue,
                        'ww mm': ww,
                        'wl mm': wl,
                        'Total Built': Total_Built,
                        'Cu surface area': conductor_surface_area,
                        'Core surface area': core_surface_area,
                        'Temperature rise Cu': temperature_rise_copper,
                        'Temperature rise Fe': temperature_rise_core,
                        'Cost': cost
                    }
                    stack_data.append(results_data)

df = pd.DataFrame(stack_data)
df 

# %%
df[df['Cost'] == df['Cost'].min()]

# %%
top_3 = []

for single_lamination in df['Lamination'].unique():
    d = df[df['Lamination'] == single_lamination]
    d_min_cost = d[d['Cost'] == d['Cost'].min()][:1]
    top_3.append({
        'x %': d_min_cost['x %'].min(),
        'Lamination': d_min_cost['Lamination'].min(),
        'Area product': d_min_cost['Area product'].min(),
        'Stack mm': d_min_cost['Stack mm'].min(),
        'Tongue mm': d_min_cost['Tongue mm'].min(),
        'wl mm': d_min_cost['wl mm'].min(),
        'ww mm': d_min_cost['ww mm'].min(),
        'Cost': d_min_cost['Cost'].min()
    })

result = pd.DataFrame(top_3).sort_values('Cost')
print(result)

# %%



