from tkinter import *
import tkinter as tk 
import pandas as pd
import numpy as np

# from task import Frequency
# print(Frequency)

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
    Ouptut_voltage = float(Output_voltage_text.get())
    Output_power = float(Output_power_text.get())
    Efficiency = float(Efficiency_text.get())
    Frequency = float(Frequency_text.get())
    B_ac = float(Flux_density_text.get())
    Regulation = float(Regulation_text.get())
    J = float(Current_density_text.get())
    K_f = 4.44
    K_u = 0.4
    Bobbin_thickness = 1.5 
    insulation_thickness = 0.2 #mm

    Apparent_power = Output_power * (1/(0.01*Efficiency) + 1)

    Area_product = (Apparent_power*(10**4))/(K_f * K_u * B_ac * J * Frequency)

    lamination_data = pd.read_csv('EI-Laminations.csv')

    # Input_current = Apparent_power / (Input_voltage * 0.01* Efficiency)
    Input_current = Output_power / Input_voltage

    A_wp = Input_current / J

    A_wp_in_sqmm = A_wp * 100   # bare area in sqcm so convert it into sqmm

    swg_data = pd.read_csv('EMD - Sheet1.csv') # select the swg the data 

    required_swg_primary = swg_data.iloc[(swg_data['Normal Conductor Area mm²'] - A_wp_in_sqmm).abs().argsort()[:1]]

    diameter_of_primary_wire_with_insulation = required_swg_primary['Medium Covering Max']

    A_wp = required_swg_primary['Normal Conductor Area mm²'].max() / 100 # cm^2

    Secondary_current = Output_power / Ouptut_voltage

    A_ws = Secondary_current / J # cm^2

    required_swg_secondary = swg_data.iloc[(swg_data['Normal Conductor Area mm²'] - A_ws * 100).abs().argsort()[:1]] 

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

                Rate_of_Cu = 950 # Rs / Kg
                Rate_of_Fe = 260 # Rs / Kg

                a = 1.68 # coefficients for core loss
                b = 1.86 # coefficients for core loss 

                # Resistivity of Cu 
                Resistivity_Cu = 1.68 * 10**-6 # ohm cm

                Iin = Input_current
                
                dw_p = diameter_of_primary_wire_with_insulation.max() 

                Turns_per_layer_primary = wl / dw_p 

                Number_of_layer_primary = Np / Turns_per_layer_primary

                Built_primary = ( Bobbin_thickness + Number_of_layer_primary * dw_p )                                      # mm

                # Built_primary = ( Bobbin_thickness + Np * dw_p ) / 10 

                MTL_primary = 2 * (tongue + stack + 2 * Built_primary + 4 * Bobbin_thickness) / 10 # cm

                Length_primary = MTL_primary * Np  # cm 

                Primary_Resistence = Resistivity_Cu * Length_primary / A_wp 

                Primary_Cu_loss = Iin**2 * Primary_Resistence

                Ns = Np * Ouptut_voltage * (1 + Regulation / 100) / Input_voltage

                Ns = round(Ns)

                Turns_per_layer_secondary = wl / diameter_of_wire_secondary_insulated 

                Number_of_layer_secondary = Ns /  Turns_per_layer_secondary  

                Built_secondary = Number_of_layer_secondary * diameter_of_wire_secondary_insulated + insulation_thickness     # mm

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

                psi = Total_loss / Total_surface_area 

                Temperature_rise = 450 * psi**0.826 

                if(ww > Total_Built):
                    result = ('Greater')
                else:
                    result = ('Lesser') 

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
                    'Total Cu Cost': Wt_of_Cu_in_kg * Rate_of_Cu,
                    'Total Fe Cost': Wt_of_core_in_kg * Rate_of_Fe,
                    'Core Area A_c cm²': A_c ,
                    # 'ww > Total Built': result,
                    'Cost': Cost,
                }
                stack_data.append(table_data_stack_and_tongue)
    
    df = pd.DataFrame(stack_data)

    print(df[df['Cost'] == df['Cost'].min()])

    cost = df[df['Cost'] == df['Cost'].min()][:1]['Cost'].max()
    cost = round(cost, 2)
    label_cost_result.delete(0, END)
    label_cost_result.insert(0, f"{cost }")

    stack = df[df['Cost'] == df['Cost'].min()][:1]['Stack mm'].max()
    label_stack_result.delete(0, END)
    label_stack_result.insert(0, f"{stack}")

    area_product = df[df['Cost'] == df['Cost'].min()][:1]['Area Product cm²'].max()
    label_area_product_result.delete(0, END)
    label_area_product_result.insert(0, f"{area_product}")

    temperature = df[df['Cost'] == df['Cost'].min()][:1]['Temperature rise'].max()
    label_temperature_rise_result.delete(0, END)
    label_temperature_rise_result.insert(0, f"{temperature}")

    lamination = df[df['Cost'] == df['Cost'].min()][:1]['Lamination'].max()
    label_lamination_result.delete(0, END)
    label_lamination_result.insert(0, f"{lamination}")

    total_copper_cost = df[df['Cost'] == df['Cost'].min()][:1]['Total Cu Cost'].max()
    label_total_copper_cost_result.delete(0, END)
    label_total_copper_cost_result.insert(0, f"{total_copper_cost}")

    total_iron_cost = df[df['Cost'] == df['Cost'].min()][:1]['Total Fe Cost'].max()
    label_total_iron_cost_result.delete(0, END)
    label_total_iron_cost_result.insert(0, f"{total_iron_cost}")
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

# 'Go' Button for getting the results
AgoButton = Button(app, text='Calculate', command=task)
AgoButton.grid(row=5, column=3, padx=5, pady=5, sticky=W)

# Calculated results 

Cost_lable = Label(app, text="Cost in Rs")
Cost_lable.grid(row=6, column=0, padx=5, pady=5, sticky=E)

lbl_cost_text = StringVar()
lbl_cost_text.set('')
label_cost_result = Entry(app, text=lbl_cost_text)
label_cost_result.grid(row=7, column=0, padx=5, pady=5, sticky=E)

stack_lable = Label(app, text="Stack mm")
stack_lable.grid(row=6, column=1, padx=5, pady=5, sticky=E)

lbl_stack_text = StringVar()
lbl_stack_text.set('')
label_stack_result = Entry(app, text=lbl_stack_text)
label_stack_result.grid(row=7, column=1, padx=5, pady=5, sticky=E)

area_product_lable = Label(app, text="Area Product cm²")
area_product_lable.grid(row=6, column=2, padx=5, pady=5, sticky=E)

lbl_area_product_text = StringVar()
lbl_area_product_text.set('')
label_area_product_result = Entry(app, text=lbl_area_product_text)
label_area_product_result.grid(row=7, column=2, padx=5, pady=5, sticky=E)

temperature_rise = Label(app, text="Temperature Rise goal")
temperature_rise.grid(row=6, column=3, padx=5, pady=5, sticky=E)

lbl_temperature_rise_text = StringVar()
lbl_temperature_rise_text.set('')
label_temperature_rise_result = Entry(app, text=lbl_temperature_rise_text)
label_temperature_rise_result.grid(row=7, column=3, padx=5, pady=5, sticky=E)

swg_required_primary_label = Label(app, text="Primary swg")
swg_required_primary_label.grid(row=8, column=0, padx=5, pady=5, sticky=E)

lbl_primary_swg = StringVar()
lbl_primary_swg.set('')
label_primary_swg_result = Entry(app, text=lbl_primary_swg)
label_primary_swg_result.grid(row=9, column=0, padx=5, pady=5, sticky=E)

swg_required_secondary_label = Label(app, text="Secondary swg")
swg_required_secondary_label.grid(row=8, column=1, padx=5, pady=5, sticky=E)

lbl_secondary_swg = StringVar()
lbl_secondary_swg.set('')
label_secondary_swg_result = Entry(app, text=lbl_secondary_swg)
label_secondary_swg_result.grid(row=9, column=1, padx=5, pady=5, sticky=E)

Lamination_label = Label(app, text="Lamination")
Lamination_label.grid(row=8, column=3, padx=5, pady=5, sticky=E)

lbl_lamination = StringVar()
lbl_lamination.set('')
label_lamination_result = Entry(app, text=lbl_lamination)
label_lamination_result.grid(row=9, column=3, padx=5, pady=5, sticky=E)

total_copper_cost_label = Label(app, text="Total copper cost Rs")
total_copper_cost_label.grid(row=10, column=0, padx=5, pady=5, sticky=E)

lbl_total_copper_cost = StringVar()
lbl_total_copper_cost.set('')
label_total_copper_cost_result = Entry(app, text=lbl_total_copper_cost)
label_total_copper_cost_result.grid(row=11, column=0, padx=5, pady=5, sticky=E)

total_iron_cost_label = Label(app, text="Total Iron Cost Rs")
total_iron_cost_label.grid(row=10, column=1, padx=5, pady=5, sticky=E)

lbl_total_iron_cost = StringVar()
lbl_total_iron_cost.set('')
label_total_iron_cost_result = Entry(app, text=lbl_total_iron_cost)
label_total_iron_cost_result.grid(row=11, column=1, padx=5, pady=5, sticky=E)

app.mainloop()

