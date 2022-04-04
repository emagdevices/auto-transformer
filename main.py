from decimal import ROUND_DOWN, ROUND_UP
from tkinter import *
import tkinter as tk 
import pandas as pd
import numpy as np
import math 
# from task import Frequency
# print(Frequency)

OPTIONS = [
"Copper",
"Aluminium"
] #etc



def task():
    Frequency = 50 # Hz
    Temperature_rise_goal = 200 # degree Celcius
    Output_power = 250 # watts
    Efficiency = 96 # %
    Input_voltage = 230 # volts
    Ouptut_voltage = 230 # volts
    Regulation = 4 # in a scale of 100
    Bobbin_thickness = 1.5 
    K_f = 4.44
    K_u = 0.4
    B_ac = 1.35
    J = 250
    insulation_thickness = 0.2 #mm

    # Input_voltage = float(Input_Voltage_text.get())
    # Ouptut_voltage = float(Output_voltage_text.get())
    # Output_power = float(Output_power_text.get())
    # Efficiency = float(Efficiency_text.get())
    # Frequency = float(Frequency_text.get())
    # B_ac = float(Flux_density_text.get())
    # Regulation = float(Regulation_text.get())
    # J = float(Current_density_text.get())
    # K_f = 4.44
    # K_u = 0.4
    # Bobbin_thickness = 1.5 
    # insulation_thickness = 0.2 #mm

    # Rate_of_Cu = float(Rate_of_Cu_text.get())
    # Rate_of_Fe = float(Rate_of_Fe_text.get())

    # Temperature_rise = float(Temperature_rise_goal_text.get())

    #pi
    pi = np.pi 

    a = 1.68 # coefficients for core loss
    b = 1.86 # coefficients for core loss 

    # Resistivity of Cu 
    # Resistivity_Cu = 1.68 * 10**-6 # ohm cm

    if conductor.get() == "Copper":
        Resistivity_conductor = 1.68 * 10**-6 # ohm cm
    if conductor.get() == "Aluminium":
        Resistivity_conductor = 2.65 * 10**-6 # ohm cm

    Resistivity_Cu = Resistivity_conductor

    Rate_of_Cu = 950 # Rs / Kg
    Rate_of_Fe = 250 # Rs / Kg
    
    

    Apparent_power = Output_power * (1/(0.01*Efficiency) + 1)

    Area_product = (Apparent_power*(10**4))/(K_f * K_u * B_ac * J * Frequency)

    lamination_data = pd.read_csv('EI-Laminations.csv')

    # Input_current = Apparent_power / (Input_voltage * 0.01* Efficiency)
    Input_current = Output_power / Input_voltage

    A_wp = Input_current / J

    A_wp_in_sqmm = A_wp * 100   # bare area in sqcm so convert it into sqmm

    swg_data = pd.read_csv('EMD - Sheet1.csv') # select the swg the data 

    higher_data = swg_data[A_wp_in_sqmm < swg_data['Normal Conductor Area mm²']]

    required_swg_primary = higher_data.iloc[(higher_data['Normal Conductor Area mm²'] - A_wp_in_sqmm).abs().argsort()[:1]]

    diameter_of_primary_wire_with_insulation = required_swg_primary['Medium Covering Max']

    A_wp = required_swg_primary['Normal Conductor Area mm²'].max() / 100 # cm^2

    Secondary_current = Output_power / Ouptut_voltage

    A_ws = Secondary_current / J # cm^2

    higher_data_swg = swg_data[A_ws * 100 < swg_data['Normal Conductor Area mm²']]

    required_swg_secondary = higher_data_swg.iloc[(higher_data_swg['Normal Conductor Area mm²'] - A_ws * 100).abs().argsort()[:1]] 

    diameter_of_wire_secondary_insulated = required_swg_secondary['Medium Covering Max'].max()                   # mm

    A_ws = required_swg_secondary['Normal Conductor Area mm²'].max() / 100  # cm^2

    # Labels for swgs and bare area
    primary_swg_version = required_swg_secondary['SWG'].max()
    label_primary_swg_result.delete(0, END)
    label_primary_swg_result.insert(0, f"{primary_swg_version}")

    secondary_swg_version = required_swg_primary['SWG'].max()
    label_secondary_swg_result.delete(0, END)
    label_secondary_swg_result.insert(0, f"{secondary_swg_version}")

    stack_data = []

    for lamination in lamination_data['Type']:
        selected_lamination = lamination_data[lamination_data['Type'] == lamination]
        for x in range(60, 141, 5):
            present_Area_product = x *0.01 *Area_product

            # Calculate stack for the present area product in cm
            stack_cm = present_Area_product * 1000 / selected_lamination['K-ratio'].max()

            stack = stack_cm * 10 # mm 
            
            if stack < 5 * selected_lamination['Tongue'].max():
                # for approximating for stack 
                if stack < 5:
                    stack = 5.0
                elif stack%5 == 0:
                    stack = stack
                elif stack%5 <= 2.5:
                    stack = stack - stack % 5
                elif stack%5 > 2.5:
                    stack = stack - stack % 5 + 5

                tongue = selected_lamination['Tongue'].max() # mm
                wl = selected_lamination['Winding-length'].max() # mm
                ww = selected_lamination['Winding-width'].max() # mm 
                A = selected_lamination['A'].max() # mm
                B = selected_lamination['B'].max() # mm
                C = selected_lamination['C'].max() # mm

                A_c = stack * selected_lamination['Tongue'].max()/100 # cm2

                Number_of_primary_turns = (Input_voltage* 10**4) / (K_f * B_ac * Frequency * A_c)

                Number_of_primary_turns = round(Number_of_primary_turns)

                Np = Number_of_primary_turns 


                Iin = Input_current
                
                dw_p = diameter_of_primary_wire_with_insulation.max() 

                Turns_per_layer_primary = math.floor( wl / dw_p) 

                Number_of_layer_primary = Np / Turns_per_layer_primary

                Built_primary = ( Bobbin_thickness + math.ceil(Number_of_layer_primary) * dw_p ) * 1.2                                      # mm

                # Built_primary = ( Bobbin_thickness + Np * dw_p ) / 10 

                MTL_primary = 2 * (tongue + stack + 2 * Built_primary + 4 * Bobbin_thickness) / 10 # cm

                Length_primary = MTL_primary * Np  # cm 

                Primary_Resistence = Resistivity_Cu * Length_primary / A_wp 

                Primary_Cu_loss = Iin**2 * Primary_Resistence

                Ns = Np * Ouptut_voltage * (1 + Regulation / 100) / Input_voltage

                Ns = round(Ns)

                Turns_per_layer_secondary = math.floor(wl / diameter_of_wire_secondary_insulated )

                Number_of_layer_secondary = math.floor(Ns /  Turns_per_layer_secondary)  

                Built_secondary = ((Number_of_layer_secondary) * diameter_of_wire_secondary_insulated + insulation_thickness  ) * 1.2   # mm

                Total_Built = Built_primary + Built_secondary

                MTL_secondary = 2 * (tongue + stack + 4 * Built_primary + 2 * Built_secondary + 4 * Bobbin_thickness) / 10    # cm

                Length_secondary = MTL_secondary * Ns 

                Secondary_Resistance = Resistivity_Cu * Length_secondary / A_ws 

                Secondary_Cu_loss = Secondary_current**2 * Secondary_Resistance

                Total_Cu_loss = Primary_Cu_loss + Secondary_Cu_loss

                Core_loss_factor = 0.000557 * Frequency**a * B_ac**b 

                volume_of_core = stack * ( B * C - 2 * ww * wl ) # mm^3

                volume_of_core_in_cm3 = volume_of_core / 1000 # cm3 

                Density_of_core = 7.65 # g/cm^3

                Wt_of_core = Density_of_core * volume_of_core_in_cm3 * 0.97 # stacking factor 

                Wt_of_core_in_kg = Wt_of_core / 1000 # kilograms

                Core_loss = Core_loss_factor* Wt_of_core_in_kg

                Total_loss = Total_Cu_loss + Core_loss

                Total_surface_area = 2 * ( B * C + B * (stack + 2 * Total_Built) + C * (stack + 2 * Total_Built) ) / 100 #cm2

                # Cu_surface area = pi * built* wl + (pi/2)* built^2 - (pi/2)*tongue^2

                Cu_surface_area = pi * Total_Built * wl + (pi/2)* Total_Built**2 - (pi/2)* tongue**2

                # Core_surface_area = 2 * ( (B*C - 2*ww*wl)+ stack*(B+C) )

                Core_surface_area = 2 * ( (B * C - 2 * ww * wl) + stack * (B+C) )

                # psi copper

                psi_copper = Total_Cu_loss / Cu_surface_area

                # psi core

                psi_core = Core_loss / Core_surface_area 

                # temperature rise in Cu

                Temperature_rise_Cu = 450 * psi_copper**0.826

                # temperature rise in Core

                Temperature_rise_Fe = 450 * psi_core**0.826

                psi = Total_loss / Total_surface_area 

                Temperature_rise = 450 * psi**0.826 

                if(ww * 0.9 > Total_Built):
                    # result = ('Greater')
                    Wt_of_Cu_in_kg = (Length_primary * required_swg_primary['Conductor Weight for 1000m/Kg'].max() + Length_secondary * required_swg_secondary['Conductor Weight for 1000m/Kg'].max() ) / 10**5

                    Cost = Wt_of_core_in_kg * Rate_of_Fe + Wt_of_Cu_in_kg * Rate_of_Cu 

                    table_data_stack_and_tongue = {
                        'Temperature rise': Temperature_rise,
                        'Area Product cm²': present_Area_product,
                        # 'A': selected_lamination['A'].max(),
                        # 'B': selected_lamination['B'].max(),
                        # 'C': selected_lamination['C'].max(),
                        'Stack mm': stack,
                        'Tongue mm': selected_lamination['Tongue'].max(),
                        'wl mm': selected_lamination['Winding-length'].max(),
                        'ww mm': selected_lamination['Winding-width'].max(),
                        'Total Built': Total_Built,
                        # 'Total Built mm': Total_Built,
                        'Lamination': selected_lamination['Type'].max(),
                        'N_p': Number_of_primary_turns,
                        'N_s': Ns,
                        'TPL P': Turns_per_layer_primary,
                        'TPL S': Turns_per_layer_secondary,
                        'Number of L P': Number_of_layer_primary,
                        'Number of L S': Number_of_layer_secondary,
                        'MTL P': MTL_primary,
                        'MTL S': MTL_secondary,
                        # 'Tongue * Stack mm²':  selected_lamination['Tongue'].max() * stack,
                        'Temperature rise Cu': Temperature_rise_Cu,
                        'Temperature rise Fe': Temperature_rise_Fe,
                        'Total Cu Cost': Wt_of_Cu_in_kg * Rate_of_Cu,
                        'Total Fe Cost': Wt_of_core_in_kg * Rate_of_Fe,
                        'Core Area A_c cm²': A_c ,
                        # 'ww > Total Built': result,
                        'Cost': Cost,
                    }
                    stack_data.append(table_data_stack_and_tongue)
    
    df = pd.DataFrame(stack_data)

    # print(df[df['Cost'] == df['Cost'].min()])

    # Entry labes for updating the inputs

    # cost = df[df['Cost'] == df['Cost'].min()][:1]['Cost'].max()
    # cost = round(cost, 2)
    # label_cost_result.delete(0, END)
    # label_cost_result.insert(0, f"{cost }")

    # stack = df[df['Cost'] == df['Cost'].min()][:1]['Stack mm'].max()
    # label_stack_result.delete(0, END)
    # label_stack_result.insert(0, f"{stack}")

    # area_product = df[df['Cost'] == df['Cost'].min()][:1]['Area Product cm²'].max()
    # label_area_product_result.delete(0, END)
    # label_area_product_result.insert(0, f"{area_product}")

    # temperature = df[df['Cost'] == df['Cost'].min()][:1]['Temperature rise'].max()
    # label_temperature_rise_result.delete(0, END)
    # label_temperature_rise_result.insert(0, f"{temperature}")

    # lamination = df[df['Cost'] == df['Cost'].min()][:1]['Lamination'].max()
    # label_lamination_result.delete(0, END)
    # label_lamination_result.insert(0, f"{lamination}")

    # total_copper_cost = df[df['Cost'] == df['Cost'].min()][:1]['Total Cu Cost'].max()
    # label_total_copper_cost_result.delete(0, END)
    # label_total_copper_cost_result.insert(0, f"{total_copper_cost}")

    # total_iron_cost = df[df['Cost'] == df['Cost'].min()][:1]['Total Fe Cost'].max()
    # label_total_iron_cost_result.delete(0, END)
    # label_total_iron_cost_result.insert(0, f"{total_iron_cost}")

    """
    For getting the top 2 results with different laminations
    """
    top_3 = []

    for i in df['Lamination'].unique():
        d = df[df['Lamination'] == i]
        d_min_cost = d[d['Cost']== d['Cost'].min()][:1] # d['Cost'].min()
        # print(d_min_cost)
        top_3.append({
            'Lamination': d_min_cost['Lamination'].min(),
            'Stack': d_min_cost['Stack mm'].min(),
            'Tongue': d_min_cost['Tongue mm'].min(),
            'wl': d_min_cost['wl mm'].min(),
            'ww': d_min_cost['ww mm'].min(),
            'Total Built': d_min_cost['Total Built'].min(),
            'Area Product cm²': d_min_cost['Area Product cm²'].min(),
            'N_p': d_min_cost['N_p'].min(),
            'N_s': d_min_cost['N_s'].min(),
            'TPL P': d_min_cost['TPL P'].min(),
            'TPL S': d_min_cost['TPL S'].min(),
            'MTL P': d_min_cost['MTL P'].min(),
            'MTL S': d_min_cost['MTL S'].min(),
            # 'Temperature rise Cu': d_min_cost['Temperature rise Cu'].min(),
            # 'Temperature rise Fe': d_min_cost['Temperature rise Fe'],
            'Temperature rise': d_min_cost['Temperature rise'].min(),
            'Total Cu Cost': d_min_cost['Total Cu Cost'].min(),
            'Total Fe Cost': d_min_cost['Total Fe Cost'].min(),
            'Cost': d_min_cost['Cost'].min()
        })

    top_3 = pd.DataFrame(top_3)
    
    top_3_sorted = top_3.sort_values(by=['Cost'])[:3]

    print(top_3_sorted)

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

    pass  



"""
UI code below 
"""
app = tk.Tk()
app.title("Auto - Transformer")

conductor = StringVar(app)
conductor.set(OPTIONS[0]) # default value

Conductor_option_lable = Label(app, text='Select Conductor')
Conductor_option_lable.grid(row=2, column=4, padx=5, pady=5, sticky=E)
Conductor_option = OptionMenu(app, conductor, *OPTIONS)
Conductor_option.grid(row=2, column=5, padx=5, pady=5, sticky=E)

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

Temperature_rise_goal_lable = Label(app, text='Temperature Rise Goal ')
Temperature_rise_goal_lable.grid(row=4, column=2, padx=5, pady=5, sticky=E)

Temperature_rise_goal_text = StringVar()
Temperature_rise_goal_text.set('')
Temperature_rise_goal_box = Entry(app, textvariable=Temperature_rise_goal_text)
Temperature_rise_goal_box.grid(row=4, column=3, padx=5, pady=5)

# 'Go' Button for getting the results
AgoButton = Button(app, text='Calculate', command=task)
AgoButton.grid(row=5, column=5, padx=5, pady=5, sticky=W)

# Calculated results 

swg_required_primary_label = Label(app, text="Primary swg")
swg_required_primary_label.grid(row=6, column=0, padx=5, pady=5, sticky=E)

lbl_primary_swg = StringVar()
lbl_primary_swg.set('')
label_primary_swg_result = Entry(app, text=lbl_primary_swg)
label_primary_swg_result.grid(row=6, column=1, padx=5, pady=5, sticky=E)

swg_required_secondary_label = Label(app, text="Secondary swg")
swg_required_secondary_label.grid(row=6, column=2, padx=5, pady=5, sticky=E)

lbl_secondary_swg = StringVar()
lbl_secondary_swg.set('')
label_secondary_swg_result = Entry(app, text=lbl_secondary_swg)
label_secondary_swg_result.grid(row=6, column=3, padx=5, pady=5, sticky=E)

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

