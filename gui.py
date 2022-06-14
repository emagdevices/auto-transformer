from decimal import ROUND_DOWN, ROUND_UP
from tkinter import *
import tkinter as tk 
import pandas as pd
import numpy as np
import math 
from input_labels import Input_Labels
# import modules 
from autotransformer import *


OPTIONS = [
"Copper",
"Aluminium"
] #etc



def lamination():
    
    # Inputs for the function3 
    spt = AutoTransformer()

    frequency = float(Frequency_text.get()) # 47  # Hz
    temperature_rise_goal = float(Temperature_rise_goal_text.get()) #  200  # celcius
    output_power = float(Output_power_text.get()) # 1000  # watts
    input_voltage = float(Input_Voltage_text.get()) # 230  # volts
    output_voltage = float(Output_voltage_text.get()) # 230  # volts
    efficiency = float(Efficiency_text.get()) # 95  # %
    regulation = float(Regulation_text.get()) # 5
    b_ac = float(Flux_density_text.get()) # 1.45  # flux density
    current_density = float(Current_density_text.get()) # 300  # amp/cm2
    Rate_of_Cu = float(Rate_of_Cu_text.get())
    Rate_of_Fe = float(Rate_of_Fe_text.get())
    # frequency = 47
    # temperature_rise_goal = 200
    # output_power = 1000
    # input_voltage = 230
    # output_voltage = 230
    # efficiency = 95
    # regulation = 5
    # b_ac = 1.45
    # current_density = 300
    # Rate_of_Cu = 950
    # Rate_of_Fe = 250
    # # standard constants
    bobbin_thickness = 1.5  # mm
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

    ##############################################################
    #                       Primary wire
    # calculate the input current
    input_current = output_power / input_voltage
    # bare area in mm2
    a_wp = spt.bare_area(input_current, current_density)
    # for primary wire
    required_strip_primary, actual_a_wp, height_priamry, width_primary = spt.find_strip_lamination(a_wp)
    #                       Primary wire
    ##############################################################   

    ##############################################################
    #                     Secondary Wire
    # calculate secondary current
    secondary_current = output_power / output_voltage
    # bare area secondary in mm2
    a_ws = spt.bare_area(secondary_current, current_density)
    required_strip_secondary, actual_a_ws, height_secondary, width_secondary = spt.find_strip_lamination(a_ws)
    #                     Secondary Wire
    ##############################################################

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

                    cost = spt.cost(weight_of_core_kg, Weight_of_copper_kg, rate_copper=Rate_of_Cu, rate_fe=Rate_of_Fe)

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
                            'Total Cu Cost': Weight_of_copper_kg * Rate_of_Cu,
                            'Total Fe Cost': weight_of_core_kg * Rate_of_Fe,
                            'Temperature rise Cu': temperature_rise_copper,
                            'Temperature rise Fe': temperature_rise_core,
                            'Cost': cost
                        }
                        stack_data.append(results_data)

    df = pd.DataFrame(stack_data)

    df[df['Cost'] == df['Cost'].min()]

    top_3 = []

    for single_lamination in df['Lamination'].unique():
        d = df[df['Lamination'] == single_lamination]
        d_min_cost = d[d['Cost'] == d['Cost'].min()][:1]
        top_3.append({
            'x %': d_min_cost['x %'].min(),
            'Lamination': d_min_cost['Lamination'].min(),
            'Area Product cm²': d_min_cost['Area product'].min(),
            'Stack': d_min_cost['Stack mm'].min(),
            'Tongue mm': d_min_cost['Tongue mm'].min(),
            'wl mm': d_min_cost['wl mm'].min(),
            'ww mm': d_min_cost['ww mm'].min(),
            'Temperature rise': d_min_cost['Temperature rise Cu'].min(),
            'Total Cu Cost': d_min_cost['Total Cu Cost'].min(),
            'Total Fe Cost': d_min_cost['Total Fe Cost'].min(),
            'Cost': d_min_cost['Cost'].min()
        })

    result = pd.DataFrame(top_3).sort_values('Cost')
    print(result)
    top_3_sorted = result

    # for lamination 1
    cost = top_3_sorted['Cost'][:1].max()
    cost = round(cost, 2)
    label_cost_result.delete(0, END)
    label_cost_result.insert(0, f"{cost }")

    stack = top_3_sorted['Stack'][:1].max()
    label_stack_result.delete(0, END)
    label_stack_result.insert(0, f"{stack}")

    area_product = top_3_sorted['Area Product cm²'][:1].max()
    label_area_product_result.delete(0, END)
    label_area_product_result.insert(0, f"{area_product}")

    temperature = top_3_sorted['Temperature rise'][:1].max()
    label_temperature_rise_result.delete(0, END)
    label_temperature_rise_result.insert(0, f"{temperature}")

    lamination = top_3_sorted['Lamination'][:1].max()
    label_lamination_result.delete(0, END)
    label_lamination_result.insert(0, f"{lamination}")

    total_copper_cost = top_3_sorted['Total Cu Cost'][:1].max()
    label_total_copper_cost_result.delete(0, END)
    label_total_copper_cost_result.insert(0, f"{total_copper_cost}")

    total_iron_cost = top_3_sorted['Total Fe Cost'][:1].max()
    label_total_iron_cost_result.delete(0, END)
    label_total_iron_cost_result.insert(0, f"{total_iron_cost}")

    # for lamination 2 
    cost2 = top_3_sorted['Cost'][1:2].max()
    cost2 = round(cost2, 2)
    label_cost_result2.delete(0, END)
    label_cost_result2.insert(0, f"{cost2 }")

    stack2 = top_3_sorted['Stack'][1:2].max()
    label_stack_result2.delete(0, END)
    label_stack_result2.insert(0, f"{stack2}")

    area_product2 = top_3_sorted['Area Product cm²'][1:2].max()
    label_area_product_result2.delete(0, END)
    label_area_product_result2.insert(0, f"{area_product2}")

    temperature2 = top_3_sorted['Temperature rise'][1:2].max()
    label_temperature_rise_result2.delete(0, END)
    label_temperature_rise_result2.insert(0, f"{temperature2}")

    lamination2 = top_3_sorted['Lamination'][1:2].max()
    label_lamination_result2.delete(0, END)
    label_lamination_result2.insert(0, f"{lamination2}")

    total_copper_cost2 = top_3_sorted['Total Cu Cost'][1:2].max()
    label_total_copper_cost_result2.delete(0, END)
    label_total_copper_cost_result2.insert(0, f"{total_copper_cost2}")

    total_iron_cost2 = top_3_sorted['Total Fe Cost'][1:2].max()
    label_total_iron_cost_result2.delete(0, END)
    label_total_iron_cost_result2.insert(0, f"{total_iron_cost2}")

    # for lamination 3
    cost3 = top_3_sorted['Cost'][2:3].max()
    cost3 = round(cost3, 2)
    label_cost_result3.delete(0, END)
    label_cost_result3.insert(0, f"{cost3 }")

    stack3 = top_3_sorted['Stack'][2:3].max()
    label_stack_result3.delete(0, END)
    label_stack_result3.insert(0, f"{stack3}")

    area_product3 = top_3_sorted['Area Product cm²'][2:3].max()
    label_area_product_result3.delete(0, END)
    label_area_product_result3.insert(0, f"{area_product3}")

    temperature3 = top_3_sorted['Temperature rise'][2:3].max()
    label_temperature_rise_result3.delete(0, END)
    label_temperature_rise_result3.insert(0, f"{temperature3}")

    lamination3 = top_3_sorted['Lamination'][2:3].max()
    label_lamination_result3.delete(0, END)
    label_lamination_result3.insert(0, f"{lamination3}")

    total_copper_cost3 = top_3_sorted['Total Cu Cost'][2:3].max()
    label_total_copper_cost_result3.delete(0, END)
    label_total_copper_cost_result3.insert(0, f"{total_copper_cost3}")

    total_iron_cost3 = top_3_sorted['Total Fe Cost'][2:3].max()
    label_total_iron_cost_result3.delete(0, END)
    label_total_iron_cost_result3.insert(0, f"{total_iron_cost3}")

"""
=================================================================
                        Strip function
We are writing function for strip with gui necessaries
=================================================================
"""

def strip():# Inputs for the function3 
    spt = AutoTransformer()

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

    frequency = 50  # Hz
    temperature_rise_goal = 100  # celcius
    output_power = 40000  # watts
    input_voltage = 230 # volts
    output_voltage = 230  # volts
    efficiency = 99  # %
    regulation = 5
    b_ac = 1.25  # flux density
    current_density = 300  # amp/cm2
    Rate_of_Cu = 950
    Rate_of_Fe = 250 

    Core_Loss_Factor = 1.5 
    bobbin_thickness = 1.5  # mm
    insulation_thickness = 0.2  # mm
    Resistivity_conductor = 1.68 * 10**-6 # ohm cm

    # from auto transformer
    k_f = spt.k_f
    k_u = spt.k_u
    lamination_data = spt.lamination_data
    swg_data = spt.swg_data
    strip_data = spt.strip_data

    # calculate the apparent power
    apparent_power = spt.apparent_power(output_power, efficiency)
    # area product
    area_product = spt.area_product(apparent_power,b_ac, current_density,frequency, k_f, k_u)
    area_product = area_product * 10**4

    ##############################################################
    #                       Primary wire
    # calculate the input current
    input_current = output_power / input_voltage
    # bare area in mm2
    a_wp = spt.bare_area(input_current, current_density)
    # for primary wire
    required_strip_primary, actual_a_wp, height_priamry, width_primary = spt.find_strip_lamination(a_wp)
    ##############################################################
    #                      Secondary Wire
    # calculate secondary current
    secondary_current = output_power / output_voltage
    # bare area secondary in mm2
    a_ws = spt.bare_area(secondary_current, current_density)
    # for secondary wire
    # required_swg_secondary, diameter_of_secondary_wire, actual_a_ws = spt.find_swg(a_ws)
    required_strip_secondary, actual_a_ws, height_secondary, width_secondary = spt.find_strip_lamination(a_ws)
    ##############################################################

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

                cost = spt.cost(weight_of_core_kg, Weight_of_copper_kg, rate_copper=Rate_of_Cu, rate_fe=Rate_of_Fe)

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

    """
    Final strip algorithm for the implementing in strip cost
    and finding the best optimized configuration
    """
    strip_data_result= []
    # algorithm
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
    print(final_result.sort_values('Cost'))
    pass


"""
UI code for app
"""

app = tk.Tk()
app.title("Auto Transformer")

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

Flux_density_lable = Label(app, text='Operational flux density Bac')
Flux_density_lable.grid(row=2, column=2, padx=5, pady=5, sticky=E)

Flux_density_text = StringVar()
Flux_density_text.set('')
Flux_density_box = Entry(app, textvariable=Flux_density_text)
Flux_density_box.grid(row=2, column=3, padx=5, pady=5)

Regulation_lable = Label(app, text='Regulation [Hz]')
Regulation_lable.grid(row=0, column=2, padx=5, pady=5, sticky=E)

Regulation_text = StringVar()
Regulation_text.set('')
Regulation_box = Entry(app, textvariable=Regulation_text)
Regulation_box.grid(row=0, column=3, padx=5, pady=5)

Current_density_lable = Label(app, text='Current Density J')
Current_density_lable.grid(row=1, column=2, padx=5, pady=5, sticky=E)

Current_density_text = StringVar()
Current_density_text.set('')
Current_density_box = Entry(app, textvariable=Current_density_text)
Current_density_box.grid(row=1, column=3, padx=5, pady=5)

Temperature_rise_goal_lable = Label(app, text='Temperature Rise Goal ')
Temperature_rise_goal_lable.grid(row=3, column=2, padx=5, pady=5, sticky=E)

Temperature_rise_goal_text = StringVar()
Temperature_rise_goal_text.set('')
Temperature_rise_goal_box = Entry(app, textvariable=Temperature_rise_goal_text)
Temperature_rise_goal_box.grid(row=3, column=3, padx=5, pady=5)

Rate_of_Cu_lable = Label(app, text='Rate of Cu [950 Rs/Kg ]')
Rate_of_Cu_lable.grid(row=0, column=4, padx=5, pady=5, sticky=E)

Rate_of_Cu_text = StringVar()
Rate_of_Cu_text.set('')
Rate_of_Cu_box = Entry(app, textvariable=Rate_of_Cu_text)
Rate_of_Cu_box.grid(row=0, column=5, padx=5, pady=5)

Rate_of_Fe_lable = Label(app, text='Rate of Fe [250 Rs/Kg ]')
Rate_of_Fe_lable.grid(row=1, column=4, padx=5, pady=5, sticky=E)

Rate_of_Fe_text = StringVar()
Rate_of_Fe_text.set('')
Rate_of_Fe_box = Entry(app, textvariable=Rate_of_Fe_text)
Rate_of_Fe_box.grid(row=1, column=5, padx=5, pady=5)

# 'Go' Button for getting the results
AgoButton = Button(app, text='Calculate', command=lamination)
AgoButton.grid(row=5, column=5, padx=5, pady=5, sticky=W)


# Lamination 

Lamination_label = Label(app, text="Lamination-I")
Lamination_label.grid(row=8, column=0, padx=5, pady=5, sticky=E)

lbl_lamination = StringVar()
lbl_lamination.set('')
label_lamination_result = Entry(app, text=lbl_lamination)
label_lamination_result.grid(row=9, column=0, padx=5, pady=5, sticky=E)

stack_lable = Label(app, text="Stack mm")
stack_lable.grid(row=8, column=2, padx=5, pady=5, sticky=E)

lbl_stack_text = StringVar()
lbl_stack_text.set('')
label_stack_result = Entry(app, text=lbl_stack_text)
label_stack_result.grid(row=9, column=2, padx=5, pady=5, sticky=E)

area_product_lable = Label(app, text="Area Product cm²")
area_product_lable.grid(row=8, column=1, padx=5, pady=5, sticky=E)

lbl_area_product_text = StringVar()
lbl_area_product_text.set('')
label_area_product_result = Entry(app, text=lbl_area_product_text)
label_area_product_result.grid(row=9, column=1, padx=5, pady=5, sticky=E)

temperature_rise = Label(app, text="Temperature Rise goal")
temperature_rise.grid(row=8, column=3, padx=5, pady=5, sticky=E)

lbl_temperature_rise_text = StringVar()
lbl_temperature_rise_text.set('')
label_temperature_rise_result = Entry(app, text=lbl_temperature_rise_text)
label_temperature_rise_result.grid(row=9, column=3, padx=5, pady=5, sticky=E)

total_copper_cost_label = Label(app, text="Total copper cost Rs")
total_copper_cost_label.grid(row=10, column=2, padx=5, pady=5, sticky=E)

lbl_total_copper_cost = StringVar()
lbl_total_copper_cost.set('')
label_total_copper_cost_result = Entry(app, text=lbl_total_copper_cost)
label_total_copper_cost_result.grid(row=11, column=2, padx=5, pady=5, sticky=E)

total_iron_cost_label = Label(app, text="Total Iron Cost Rs")
total_iron_cost_label.grid(row=10, column=1, padx=5, pady=5, sticky=E)

lbl_total_iron_cost = StringVar()
lbl_total_iron_cost.set('')
label_total_iron_cost_result = Entry(app, text=lbl_total_iron_cost)
label_total_iron_cost_result.grid(row=11, column=1, padx=5, pady=5, sticky=E)

Cost_lable = Label(app, text="Total Cost in Rs")
Cost_lable.grid(row=10, column=3, padx=5, pady=5, sticky=E)

lbl_cost_text = StringVar()
lbl_cost_text.set('')
label_cost_result = Entry(app, text=lbl_cost_text)
label_cost_result.grid(row=11, column=3, padx=5, pady=5, sticky=E)

# For second 

Lamination_label2 = Label(app, text="Lamination-II")
Lamination_label2.grid(row=20, column=0, padx=5, pady=5, sticky=E)

lbl_lamination2 = StringVar()
lbl_lamination2.set('')
label_lamination_result2 = Entry(app, text=lbl_lamination2)
label_lamination_result2.grid(row=21, column=0, padx=5, pady=5, sticky=E)

stack_lable2 = Label(app, text="Stack mm")
stack_lable2.grid(row=20, column=2, padx=5, pady=5, sticky=E)

lbl_stack_text2 = StringVar()
lbl_stack_text2.set('')
label_stack_result2 = Entry(app, text=lbl_stack_text2)
label_stack_result2.grid(row=21, column=2, padx=5, pady=5, sticky=E)

area_product_lable2 = Label(app, text="Area Product cm²")
area_product_lable2.grid(row=20, column=1, padx=5, pady=5, sticky=E)

lbl_area_product_text2 = StringVar()
lbl_area_product_text2.set('')
label_area_product_result2 = Entry(app, text=lbl_area_product_text2)
label_area_product_result2.grid(row=21, column=1, padx=5, pady=5, sticky=E)

temperature_rise2 = Label(app, text="Temperature Rise goal")
temperature_rise2.grid(row=20, column=3, padx=5, pady=5, sticky=E)

lbl_temperature_rise_text2 = StringVar()
lbl_temperature_rise_text2.set('')
label_temperature_rise_result2 = Entry(app, text=lbl_temperature_rise_text2)
label_temperature_rise_result2.grid(row=21, column=3, padx=5, pady=5, sticky=E)

total_copper_cost_label2 = Label(app, text="Total copper cost Rs")
total_copper_cost_label2.grid(row=22, column=2, padx=5, pady=5, sticky=E)

lbl_total_copper_cost2 = StringVar()
lbl_total_copper_cost2.set('')
label_total_copper_cost_result2 = Entry(app, text=lbl_total_copper_cost2)
label_total_copper_cost_result2.grid(row=23, column=2, padx=5, pady=5, sticky=E)

total_iron_cost_label2 = Label(app, text="Total Iron Cost Rs")
total_iron_cost_label2.grid(row=22, column=1, padx=5, pady=5, sticky=E)

lbl_total_iron_cost2 = StringVar()
lbl_total_iron_cost2.set('')
label_total_iron_cost_result2 = Entry(app, text=lbl_total_iron_cost2)
label_total_iron_cost_result2.grid(row=23, column=1, padx=5, pady=5, sticky=E)

Cost_lable2 = Label(app, text="Total Cost in Rs")
Cost_lable2.grid(row=22, column=3, padx=5, pady=5, sticky=E)

lbl_cost_text2 = StringVar()
lbl_cost_text2.set('')
label_cost_result2 = Entry(app, text=lbl_cost_text2)
label_cost_result2.grid(row=23, column=3, padx=5, pady=5, sticky=E)

# lamination 3

Lamination_label3 = Label(app, text="Lamination-III")
Lamination_label3.grid(row=30, column=0, padx=5, pady=5, sticky=E)

lbl_lamination3 = StringVar()
lbl_lamination3.set('')
label_lamination_result3 = Entry(app, text=lbl_lamination3)
label_lamination_result3.grid(row=31, column=0, padx=5, pady=5, sticky=E)

stack_lable3 = Label(app, text="Stack mm")
stack_lable3.grid(row=30, column=2, padx=5, pady=5, sticky=E)

lbl_stack_text3 = StringVar()
lbl_stack_text3.set('')
label_stack_result3 = Entry(app, text=lbl_stack_text3)
label_stack_result3.grid(row=31, column=2, padx=5, pady=5, sticky=E)

area_product_lable3 = Label(app, text="Area Product cm²")
area_product_lable3.grid(row=30, column=1, padx=5, pady=5, sticky=E)

lbl_area_product_text3 = StringVar()
lbl_area_product_text3.set('')
label_area_product_result3 = Entry(app, text=lbl_area_product_text3)
label_area_product_result3.grid(row=31, column=1, padx=5, pady=5, sticky=E)

temperature_rise3 = Label(app, text="Temperature Rise goal")
temperature_rise3.grid(row=30, column=3, padx=5, pady=5, sticky=E)

lbl_temperature_rise_text3 = StringVar()
lbl_temperature_rise_text3.set('')
label_temperature_rise_result3 = Entry(app, text=lbl_temperature_rise_text3)
label_temperature_rise_result3.grid(row=31, column=3, padx=5, pady=5, sticky=E)

total_copper_cost_label3 = Label(app, text="Total copper cost Rs")
total_copper_cost_label3.grid(row=32, column=2, padx=5, pady=5, sticky=E)

lbl_total_copper_cost3 = StringVar()
lbl_total_copper_cost3.set('')
label_total_copper_cost_result3 = Entry(app, text=lbl_total_copper_cost3)
label_total_copper_cost_result3.grid(row=33, column=2, padx=5, pady=5, sticky=E)

total_iron_cost_label3 = Label(app, text="Total Iron Cost Rs")
total_iron_cost_label3.grid(row=32, column=1, padx=5, pady=5, sticky=E)

lbl_total_iron_cost3 = StringVar()
lbl_total_iron_cost3.set('')
label_total_iron_cost_result3 = Entry(app, text=lbl_total_iron_cost3)
label_total_iron_cost_result3.grid(row=33, column=1, padx=5, pady=5, sticky=E)

Cost_lable3 = Label(app, text="Total Cost in Rs")
Cost_lable3.grid(row=32, column=3, padx=5, pady=5, sticky=E)

lbl_cost_text3 = StringVar()
lbl_cost_text3.set('')
label_cost_result3 = Entry(app, text=lbl_cost_text3)
label_cost_result3.grid(row=33, column=3, padx=5, pady=5, sticky=E)


app.mainloop()



if __name__ == '__main__':
    strip()