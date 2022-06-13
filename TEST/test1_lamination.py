# Inputs for the function3 
# %%
from autotransformer import AutoTransformer
import pandas as pd
import math 
spt = AutoTransformer()

# frequency = float(self.frequency.label_text.get()) # 47  # Hz
# temperature_rise_goal = float(self.temperature_rise.label_text.get()) #  200  # celcius
# output_power = float(self.output_power.label_text.get()) # 1000  # watts
# input_voltage = float(self.input_voltage.label_text.get()) # 230  # volts
# output_voltage = float(self.output_voltage.label_text.get()) # 230  # volts
# efficiency = float(self.efficiency.label_text.get()) # 95  # %
# regulation = float(self.regulation.label_text.get()) # 5
# b_ac = float(self.flux_density.label_text.get()) # 1.45  # flux density
# current_density = float(self.current_density.label_text.get()) # 300  # amp/cm2
# Rate_of_Cu = float(self.rate_of_Cu.label_text.get())
# Rate_of_Fe = float(self.rate_of_Fe.label_text.get())

# frequency = float(Frequency_text.get()) # 47  # Hz
# temperature_rise_goal = float(Temperature_rise_goal_text.get()) #  200  # celcius
# output_power = float(Output_power_text.get()) # 1000  # watts
# input_voltage = float(Input_Voltage_text.get()) # 230  # volts
# output_voltage = float(Output_voltage_text.get()) # 230  # volts
# efficiency = float(Efficiency_text.get()) # 95  # %
# regulation = float(Regulation_text.get()) # 5
# b_ac = float(Flux_density_text.get()) # 1.45  # flux density
# current_density = float(Current_density_text.get()) # 300  # amp/cm2
# Rate_of_Cu = float(Rate_of_Cu_text.get())
# Rate_of_Fe = float(Rate_of_Fe_text.get())
# %%
frequency = 50
temperature_rise_goal = 200
output_power = 10
input_voltage = 230
output_voltage = 10
efficiency = 90
regulation = 4
b_ac = 1.25
current_density = 250
Rate_of_Cu = 950
Rate_of_Fe = 140
# # standard constants
bobbin_thickness = spt.calculate_bobbin_thicness(output_power)  # mm
insulation_thickness = 0.2  # mm
Resistivity_conductor = 1.68 * 10**-6 # ohm cm
# core loss factor as new input variable
Core_Loss_Factor = 1.5 
# from auto transformer
k_f = spt.k_f
k_u = spt.k_u
lamination_data = spt.lamination_data
swg_data = pd.read_csv('https://raw.githubusercontent.com/emagdevices/auto-transformer/main/DATA/Wires_data.csv')

apparent_power = spt.apparent_power(output_power, efficiency)
area_product = spt.area_product(apparent_power,b_ac, current_density,frequency, k_f, k_u)
# %%
##############################################################
#                       Primary wire
# calculate the input current
input_current = output_power / input_voltage
# bare area in mm2
a_wp = spt.bare_area(input_current, current_density)
# for primary wire
required_strip_primary, actual_a_wp, height_priamry, width_primary = spt.find_strip_lamination(a_wp)
print('Primary wire: ')
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
required_strip_secondary, actual_a_ws, height_secondary, width_secondary = spt.find_strip_lamination(a_ws)

print('Secondary wire: ')
print(required_strip_secondary)
#                     Secondary Wire
##############################################################

# %%
stack_data = []

# %%
for lamination in lamination_data['Type']:

    selected_lamination = lamination_data[lamination_data['Type'] == lamination]

    for x in range(60, 141, 5):

        tongue = selected_lamination['Tongue'].max()  # mm

        wl = selected_lamination['Winding-length'].max() # mm
        
        ww = selected_lamination['Winding-width'].max() # mm 

        present_area_product = x * 0.01 * area_product

        stack = spt.calculate_stack(present_area_product, selected_lamination['K-ratio'].max())

        if stack < 2 * tongue and stack > tongue * 0.5:

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

                Density_of_core = 7.8 # g/cm^3

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

                cost = spt.cost(weight_of_core_kg, Weight_of_copper_kg, rate_copper=Rate_of_Cu, rate_fe=Rate_of_Fe)

                if (temperature_rise_copper < temperature_rise_goal) and (temperature_rise_core < temperature_rise_goal):
                    results_data = {
                        'x %': x,
                        'Lamination': selected_lamination['Type'].max(),
                        'Area product': present_area_product,
                        'Primary wire': required_strip_primary['combination'].min(),
                        'width primary': width_primary,
                        'height primary': height_priamry,
                        'Secondary wire': required_strip_secondary['combination'].min(),
                        'width secondary': width_secondary,
                        'height secondary': height_secondary,
                        'Stack mm': stack,
                        'Tongue mm': tongue,
                        'ww mm': ww,
                        'wl mm': wl,
                        'Primary turns': Number_of_primary_turns,
                        'Secondary turns': Number_of_secondary_turns,
                        'Total Built': Total_Built,
                        'Cu surface area': conductor_surface_area,
                        'Core surface area': core_surface_area,
                        'Core Loss': core_loss,
                        'Copper Loss': Total_Cu_loss,
                        'Total Cu Cost': Weight_of_copper_kg * Rate_of_Cu,
                        'Total Fe Cost': weight_of_core_kg * Rate_of_Fe,
                        'Temperature rise Cu': temperature_rise_copper,
                        'Temperature rise Fe': temperature_rise_core,
                        'Core weight': weight_of_core_kg,
                        'Conductor weight': Weight_of_copper_kg,
                        'Cost': cost
                    }
                    stack_data.append(results_data)

df = pd.DataFrame(stack_data)


# %% 
if df.empty:
    df = pd.DataFrame(
        {
            'x %': [],
            'Lamination': [],
            'Area product': [],
            'Primary wire': [],
            'width primary': [],
            'height primary': [],
            'Secondary wire': [],
            'width secondary': [],
            'height secondary': [],
            'Stack mm': [],
            'Tongue mm': [],
            'ww mm': [],
            'wl mm': [],
            'Primary turns': [],
            'Secondary turns': [],
            'Total Built': [],
            'Cu surface area': [],
            'Core surface area': [],
            'Core Loss': [],
            'Copper Loss': [],
            'Total Cu Cost': [],
            'Total Fe Cost': [],
            'Temperature rise Cu': [],
            'Temperature rise Fe': [],
            'Core weight': [],
            'Conductor weight': [],
            'Cost': []
        }
    ) 

# %%
top_3 = []
for single_lamination in df['Lamination'].unique():
    d = df[df['Lamination'] == single_lamination]
    d_min_cost = d[d['Cost'] == d['Cost'].min()][:1]
    top_3.append({
        # 'x %': d_min_cost['x %'].min(),
        # 'Lamination': d_min_cost['Lamination'].min(),
        # 'Area Product cm²': d_min_cost['Area product'].min(),
        'Type': 'Lamination ',
        # 'Primary wire': d_min_cost['Primary wire'].min(),
        # 'width primary': d_min_cost['width primary'].min(),
        # 'height primary': d_min_cost['height primary'].min(),
        # 'Secondary wire': d_min_cost['Secondary wire'].min(),
        # 'width secondary': d_min_cost['width secondary'].min(),
        # 'height secondary': d_min_cost['height secondary'].min(),
        'Stack mm': d_min_cost['Stack mm'].min(),
        'Tongue mm': d_min_cost['Tongue mm'].min(),
        'wl mm': d_min_cost['wl mm'].min(),
        'ww mm': d_min_cost['ww mm'].min(),
        'Primary turns': d_min_cost['Primary turns'].min(),
        'Secondary turns': d_min_cost['Secondary turns'].min(),
        'Total Built': d_min_cost['Total Built'].min(),
        'Core Loss': d_min_cost['Core Loss'].min(),
        'Copper Loss': d_min_cost['Copper Loss'].min(),
        'Temperature rise Cu': d_min_cost['Temperature rise Cu'].min(),
        'Temperature rise Fe': d_min_cost['Temperature rise Fe'].min(),
        # 'Total Cu Cost': d_min_cost['Total Cu Cost'].min(),
        # 'Total Fe Cost': d_min_cost['Total Fe Cost'].min(),
        'Core weight': d_min_cost['Core weight'].min(),
        'Conductor weight': d_min_cost['Conductor weight'].min(),
        'Cost': d_min_cost['Cost'].min()
    })

result = pd.DataFrame(top_3).sort_values('Cost')
print(result)
top_3_sorted = result
