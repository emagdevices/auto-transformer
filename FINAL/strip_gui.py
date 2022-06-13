# from tkinter import StringVar, Tk, Label, Button, Entry
from re import M
from tkinter import *
# from FINAL.gui import lamination
from autotransformer import AutoTransformer
import math 
import pandas as pd 

class StripGUI:
    def __init__(self, master):
        self.master = master
        master.title("Auto Transformer Strip Calculation")

        self.label = Label(master, text="Strip Calculation")
        self.label.grid(row=2, column=1)

        """
        For simply changing the base row we need to make sure 
        to keep a certain base row from which we start adding our labels.
        It also helps in adding new inputs later
        """
        self.n = 3  

        self.input_voltage = Input_Label(master,
            'Input voltage [volts]',
            self.n,
            0)


        self.output_voltage = Input_Label(master,
            'Output voltage [volts]',
            self.n + 1,
            0)

        self.output_power = Input_Label(master,
            'Output Power [watts]',
            self.n + 2,
            0)

        self.efficiency = Input_Label(master,
            'Efficienty [100%]',
            self.n + 3,
            0)

        self.frequency = Input_Label(master,
            'Frequency [Hz]',
            self.n + 4, 0)

        self.flux_density = Input_Label(master, 
            'Operational flux density Bac',
            self.n,
            3)

        self.regulation = Input_Label(master, 
            'Regulation',
            self.n + 1,
            3)

        self.current_density = Input_Label(master,
            'Current Density J',
            self.n + 2,
            3)

        self.temperature_rise = Input_Label(master,
            'Temperature Rise Goal',
            self.n + 3,
            3)

        self.rate_of_Cu = Input_Label(master,
            'Rate of Cu [950 Rs/Kg]',
            self.n,
            5)
        
        self.rate_of_Fe = Input_Label(master,
            'Rate of Fe [250 Rs/K]',
            self.n + 1,
            5)
        """
        ================================================================
                            Lamination Output Labels
        ================================================================
        """
        self.primary_wire = Output_Label(
            master,
            'Primary Wire',
            self.n + 7,
            1
        )

        self.height_primary = Output_Label(
            master,
            'Height Primary',
            self.n + 7,
            2
        )
        self.width_primary = Output_Label(
            master,
            'Width Primary',
            self.n + 7,
            3
        )
        self.secondary_wire = Output_Label(
            master,
            'Secondary Wire',
            self.n + 7,
            4
        )
        self.height_secondary = Output_Label(
            master,
            'Height Secondary',
            self.n + 7,
            5
        )
        self.width_secondary = Output_Label(
            master,
            'Width Secondary',
            self.n + 7,
            6
        )

        
        """
        ================================================================
                            Lamination Output Labels
        ================================================================
        """
        # self.n = self.n + 10

        # # here lamination one
        # self.lamination_I = Lamination_Output(master, 1, self.n, 0)

        # # here lamination two
        # self.lamination_II = Lamination_Output(master, 2, self.n + 4, 0)

        # # here lamiantion threee
        # self.lamination_III = Lamination_Output(master, 3, self.n + 8, 0)
        
        """
        ================================================================
                              Strip Output Labels
        ================================================================
        """
        self.n = self.n + 15

        self.strip_I = Strip_Output(master, 1, self.n, self.data)

        self.strip_II = Strip_Output(master, 2, self.n + 4, self.data)

        self.strip_III = Strip_Output(master, 3, self.n + 8, self.data)

        self.strip_IV = Strip_Output(master, 3, self.n + 12, self.data)

        self.strip_V = Strip_Output(master, 5, self.n + 16, self.data)

        self.strip_VI = Strip_Output(master, 6, self.n + 20, self.data)

        self.strip_VII = Strip_Output(master, 7, self.n + 24, self.data)

        self.strip_VIII = Strip_Output(master, 8, self.n + 28, self.data)

        self.strip_IX = Strip_Output(master, 9, self.n + 32, self.data)

        self.strip_X = Strip_Output(master, 10, self.n + 36, self.data)

        self.strip_XI = Strip_Output(master, 11, self.n + 40, self.data)

        self.strip_XII = Strip_Output(master, 12, self.n + 44, self.data)

        self.strip_XIII = Strip_Output(master, 13, self.n + 48, self.data)

        self.strip_XIV = Strip_Output(master, 14, self.n + 52, self.data)

        self.strip_XV = Strip_Output(master, 15, self.n + 56, self.data)

        """
        ================================================================
                                        Buttons
        ================================================================
        """
        self.strip_button = Button(master, text="Calculate Strip", command=self.both)
        self.strip_button.grid(row=0, column=9)

        """
        ================================================================
                                     Close Button
        ================================================================
        """
        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.grid(row=0, column=10)


    def strip(self):
        
        spt = AutoTransformer()

        frequency = float(self.frequency.label_text.get()) # 47  # Hz
        temperature_rise_goal = float(self.temperature_rise.label_text.get()) #  200  # celcius
        output_power = float(self.output_power.label_text.get()) # 1000  # watts
        input_voltage = float(self.input_voltage.label_text.get()) # 230  # volts
        output_voltage = float(self.output_voltage.label_text.get()) # 230  # volts
        efficiency = float(self.efficiency.label_text.get()) # 95  # %
        regulation = float(self.regulation.label_text.get()) # 5
        b_ac = float(self.flux_density.label_text.get()) # 1.45  # flux density
        current_density = float(self.current_density.label_text.get()) # 300  # amp/cm2
        Rate_of_Cu = float(self.rate_of_Cu.label_text.get())
        Rate_of_Fe = float(self.rate_of_Fe.label_text.get())

        # frequency = 50
        # temperature_rise_goal = 200
        # output_power = 10
        # input_voltage = 230
        # output_voltage = 10
        # efficiency = 85
        # regulation = 5
        # b_ac = 1.25
        # current_density = 250
        # Rate_of_Cu = 950
        # Rate_of_Fe = 250

        # standard constants
        Core_Loss_Factor = 1.5 
        bobbin_thickness = spt.calculate_bobbin_thicness(output_power)  # mm
        insulation_thickness = 0.2  # mm
        Resistivity_conductor = 1.68 * 10**-6 # ohm cm
        k_f = spt.k_f
        k_u = spt.k_u

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
            
            if stack < 2 * tongue and stack > tongue * 0.5:

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

                    Density_of_core = 7.8 # g/cm^3

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
                            'Type': 'S/U',
                            'Primary wire': required_strip_primary['combination'].min(),
                            'width primary': width_primary,
                            'height primary': height_priamry,
                            'Secondary wire': required_strip_secondary['combination'].min(),
                            'width secondary': width_secondary,
                            'height secondary': height_secondary,
                            'Stack mm': stack,
                            'Tongue mm': tongue,
                            'wl mm': winding_lenghth,
                            'ww mm': winding_width,
                            'Total Built': Total_Built,
                            'Core Loss': core_loss,
                            'Copper Loss': Total_Cu_loss,
                            'Temperature rise Cu': temperature_rise_copper,
                            'Temperature rise Fe': temperature_rise_core,
                            'Core weight': weight_of_core_kg,
                            'Conductor weight': Weight_of_copper_kg,
                            'Cost': cost,
                            'Primary turns': Number_of_primary_turns,
                            'Secondary turns': Number_of_secondary_turns,
                            'MTL Primary': MTL_primary,
                            'MTL Secondary': MTL_secondary,
                            'TPL Primary': Turns_per_layer_primary,
                            'TPL Secondary': Turns_per_layer_secondary,
                            'Length primary': Length_primary,
                            'Length secondary': Length_secondary,
                            'Resistance primary': Primary_resistance,
                            'Resistance secondary': Secondary_resistance,
                            'Cu surface area': conductor_surface_area,
                            'Core surface area': core_surface_area,
                            'Weight of Cu kg': Weight_of_copper_kg,
                            'Weight of Fe': weight_of_core_kg
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
                if stack < 2 * tongue and stack > 0.8 * tongue:
                    for ww in range(20, 250, 5):
                        for wl in range(120, 600, 5):
                            product = stack * tongue * ww * wl 
                            if area_product * 1.5 > product and area_product * 0.5 < product:
                                results = strip_cost(stack, tongue, ww, wl)
                                if results:
                                    strip_data_result.append(results)

        final_result = pd.DataFrame(strip_data_result)
        if final_result.empty:
            final_result = pd.DataFrame({
                'Type': 'S/U',
                'Primary wire': [],
                'width primary': [],
                'height primary': [],
                'Secondary wire': [],
                'width secondary': [],
                'height secondary': [],
                'Stack mm': [],
                'Tongue mm': [],
                'wl mm': [],
                'ww mm': [],
                'Total Built': [],
                'Core Loss': [],
                'Copper Loss': [],
                'Temperature rise Cu': [],
                'Temperature rise Fe': [],
                'Core weight': [],
                'Conductor weight': [],
                'Cost': [],
                'Primary turns': [],
                'Secondary turns': [],
                'MTL Primary': [],
                'MTL Secondary': [],
                'TPL Primary': [],
                'TPL Secondary': [],
                'Length primary': [],
                'Length secondary': [],
                'Resistance primary': [],
                'Resistance secondary': [],
                'Cu surface area': [],
                'Core surface area': [],
                'Weight of Cu kg': [],
                'Weight of Fe': []
            })
        else:
            final_result = final_result.sort_values('Cost')
        print(final_result.sort_values('Cost'))
        # print(final_result)

        # cost = round(final_result['Cost'].min(), 3)
        # self.cost.label_result.delete(0, END)
        # self.cost.label_result.insert(0, f'{cost}')

        return final_result


    def lamination(self):
        # Inputs for the function3 
        spt = AutoTransformer()

        frequency = float(self.frequency.label_text.get()) # 47  # Hz
        temperature_rise_goal = float(self.temperature_rise.label_text.get()) #  200  # celcius
        output_power = float(self.output_power.label_text.get()) # 1000  # watts
        input_voltage = float(self.input_voltage.label_text.get()) # 230  # volts
        output_voltage = float(self.output_voltage.label_text.get()) # 230  # volts
        efficiency = float(self.efficiency.label_text.get()) # 95  # %
        regulation = float(self.regulation.label_text.get()) # 5
        b_ac = float(self.flux_density.label_text.get()) # 1.45  # flux density
        current_density = float(self.current_density.label_text.get()) # 300  # amp/cm2
        Rate_of_Cu = float(self.rate_of_Cu.label_text.get())
        Rate_of_Fe = float(self.rate_of_Fe.label_text.get())

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

        stack_data = []

        for lamination in lamination_data['Type']:

            selected_lamination = lamination_data[lamination_data['Type'] == lamination]

            for x in range(60, 141, 5):

                tongue = selected_lamination['Tongue'].max()  # mm

                wl = selected_lamination['Winding-length'].max() # mm
                
                ww = selected_lamination['Winding-width'].max() # mm 

                present_area_product = x * 0.01 * area_product

                stack = spt.calculate_stack(present_area_product, selected_lamination['K-ratio'].max())

                print(f'lamination: {lamination} >> area product: {present_area_product} >> stack: {stack} >> tongue: {tongue}')

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
                                # 'x %': x,
                                'Lamination': selected_lamination['Type'].max(),
                                # 'Area product': present_area_product,
                                'Type': 'Lamination',
                                'Primary wire': required_strip_primary['combination'].min(),
                                'width primary': width_primary,
                                'height primary': height_priamry,
                                'Secondary wire': required_strip_secondary['combination'].min(),
                                'width secondary': width_secondary,
                                'height secondary': height_secondary,
                                'Stack mm': stack,
                                'Tongue mm': tongue,
                                'wl mm': wl,
                                'ww mm': ww,
                                'Total Built': Total_Built,
                                'Core Loss': core_loss,
                                'Copper Loss': Total_Cu_loss,
                                # 'Total Cu Cost': Weight_of_copper_kg * Rate_of_Cu,
                                # 'Total Fe Cost': weight_of_core_kg * Rate_of_Fe,
                                'Temperature rise Cu': temperature_rise_copper,
                                'Temperature rise Fe': temperature_rise_core,
                                'Core weight': weight_of_core_kg,
                                'Conductor weight': Weight_of_copper_kg,
                                'Cost': cost,
                                'Primary turns': Number_of_primary_turns,
                                'Secondary turns': Number_of_secondary_turns,
                                'MTL Primary': MTL_primary,
                                'MTL Secondary': MTL_secondary,
                                'TPL Primary': Turns_per_layer_primary,
                                'TPL Secondary': Turns_per_layer_secondary,
                                'Length primary': Length_primary,
                                'Length secondary': Length_secondary,
                                'Resistance primary': Primary_resistance,
                                'Resistance secondary': Secondary_resistance,
                                'Cu surface area': conductor_surface_area,
                                'Core surface area': core_surface_area,
                                'Weight of Cu kg': Weight_of_copper_kg,
                                'Weight of Fe': weight_of_core_kg
                            }
                            stack_data.append(results_data)

        df = pd.DataFrame(stack_data)
        if df.empty:
            df = pd.DataFrame({
                'Lamination': [],
                'Type': [],
                'Primary wire': [],
                'width primary': [],
                'height primary': [],
                'Secondary wire': [],
                'width secondary': [],
                'height secondary': [],
                'Stack mm': [],
                'Tongue mm': [],
                'wl mm': [],
                'ww mm': [],
                'Total Built': [],
                'Core Loss': [],
                'Copper Loss': [],
                'Temperature rise Cu': [],
                'Temperature rise Fe': [],
                'Core weight': [],
                'Conductor weight': [],
                'Cost': [],
                'Primary turns': [],
                'Secondary turns': [],
                'MTL Primary': [],
                'MTL Secondary': [],
                'TPL Primary': [],
                'TPL Secondary': [],
                'Length primary': [],
                'Length secondary': [],
                'Resistance primary': [],
                'Resistance secondary': [],
                'Cu surface area': [],
                'Core surface area': [],
                'Weight of Cu kg': [],
                'Weight of Fe': []
            })

        print(df)

        top = df.sort_values('Cost').groupby('Lamination').first().sort_values('Cost')


        top_3 = []
        for single_lamination in df['Lamination'].unique():
            d = df[df['Lamination'] == single_lamination]
            d_min_cost = d[d['Cost'] == d['Cost'].min()][:1]
            top_3.append({
                # 'x %': d_min_cost['x %'].min(),
                # 'Lamination': d_min_cost['Lamination'].min(),
                # 'Area Product cm²': d_min_cost['Area product'].min(),
                'Type': 'Lamination ',
                'Primary wire': d_min_cost['Primary wire'].min(),
                'width primary': d_min_cost['width primary'].min(),
                'height primary': d_min_cost['height primary'].min(),
                'Secondary wire': d_min_cost['Secondary wire'].min(),
                'width secondary': d_min_cost['width secondary'].min(),
                'height secondary': d_min_cost['height secondary'].min(),
                'Stack mm': d_min_cost['Stack mm'].min(),
                'Tongue mm': d_min_cost['Tongue mm'].min(),
                'wl mm': d_min_cost['wl mm'].min(),
                'ww mm': d_min_cost['ww mm'].min(),
                'Total Built': d_min_cost['Total Built'].min(),
                'Core Loss': d_min_cost['Core Loss'].min(),
                'Copper Loss': d_min_cost['Copper Loss'].min(),
                'Temperature rise Cu': d_min_cost['Temperature rise Cu'].min(),
                'Temperature rise Fe': d_min_cost['Temperature rise Fe'].min(),
                # 'Total Cu Cost': d_min_cost['Total Cu Cost'].min(),
                # 'Total Fe Cost': d_min_cost['Total Fe Cost'].min(),
                'Core weight': d_min_cost['Core weight'].min(),
                'Conductor weight': d_min_cost['Conductor weight'].min(),
                'Cost': d_min_cost['Cost'].min(),
                'Primary turns': d_min_cost['Primary turns'].min(),
                'Secondary turns': d_min_cost['Secondary turns'].min(),
                'MTL Primary': d_min_cost['MTL Primary'].min(),
                'MTL Secondary': d_min_cost['MTL Secondary'].min(),
                'TPL Primary': d_min_cost['TPL Primary'].min(),
                'TPL Secondary': d_min_cost['TPL Secondary'].min(),
                'Length primary': d_min_cost['Length primary'].min(),
                'Length secondary': d_min_cost['Length secondary'].min(),
                'Resistance primary': d_min_cost['Resistance primary'].min(),
                'Resistance secondary': d_min_cost['Resistance secondary'].min(),
                'Cu surface area': d_min_cost['Cu surface area'].min(),
                'Core surface area': d_min_cost['Core surface area'].min(),
                'Weight of Cu kg': d_min_cost['Weight of Cu kg'].min(),
                'Weight of Fe': d_min_cost['Weight of Fe'].min()
            })
        if len(top_3) == 0:
            top_3 = pd.DataFrame({
                'Lamination': [],
                'Type': [],
                'Primary wire': [],
                'width primary': [],
                'height primary': [],
                'Secondary wire': [],
                'width secondary': [],
                'height secondary': [],
                'Stack mm': [],
                'Tongue mm': [],
                'wl mm': [],
                'ww mm': [],
                'Total Built': [],
                'Core Loss': [],
                'Copper Loss': [],
                'Temperature rise Cu': [],
                'Temperature rise Fe': [],
                'Core weight': [],
                'Conductor weight': [],
                'Cost': [],
                'Primary turns': [],
                'Secondary turns': [],
                'MTL Primary': [],
                'MTL Secondary': [],
                'TPL Primary': [],
                'TPL Secondary': [],
                'Length primary': [],
                'Length secondary': [],
                'Resistance primary': [],
                'Resistance secondary': [],
                'Cu surface area': [],
                'Core surface area': [],
                'Weight of Cu kg': [],
                'Weight of Fe': []
            })

        result = pd.DataFrame(top_3).sort_values('Cost')
        print(result)
        top_3_sorted = result
        return top_3_sorted

    def data(self):
        data = pd.read_csv('/home/yash7/Desktop/EMD/auto-transformer/FINAL/results.csv')
        print(data)
        pass 

    def both(self):
        df1 = self.lamination()
        # print(df1)
        df2 = self.strip()
        results = pd.concat([df1, df2])
        # results = df2 
        print(results)
        print(results.columns)
        # print(results['Total Built'])

        results.to_csv('/home/yash7/Desktop/EMD/auto-transformer/FINAL/results.csv')

        pw = results['Primary wire'][0:1].min()
        self.primary_wire.label_result.delete(0, END)
        self.primary_wire.label_result.insert(0, f'{pw}')
        hp = results['height primary'][0:1].min()
        self.height_primary.label_result.delete(0, END)
        self.height_primary.label_result.insert(0, f'{hp}')
        wp = results['width primary'][0:1].min()
        self.width_primary.label_result.delete(0, END)
        self.width_primary.label_result.insert(0, f'{wp}')
        sw = results['Secondary wire'][0:1].min()
        GetDataToLabel(self.secondary_wire, sw)
        hs = results['height secondary'][0:1].min()
        GetDataToLabel(self.height_secondary, hs)
        ws = results['width secondary'][0:1].min()
        GetDataToLabel(self.width_secondary, ws)


        stripArray = [self.strip_I, self.strip_II, self.strip_III, self.strip_IV, 
        self.strip_V, self.strip_VI, self.strip_VII, self.strip_VIII, self.strip_IX, 
        self.strip_X, self.strip_XI, self.strip_XII, self.strip_XIII, self.strip_XIV,
        self.strip_XV]
        # cost = GetParameterData(stripArray, results['Cost'])
        n = 0
        for strip in stripArray:
            GetTypeData(strip, results[0+n:1+n])
            n = n + 1

  


class Input_Label:
    def __init__(self, master, text, Row, Column):
        self.label = Label(master, text=text)
        self.label.grid(row=Row, column=Column)
        self.label_text = StringVar()
        self.label_text.set('')
        self.label_result = Entry(master, textvariable=self.label_text)
        self.label_result.grid(row=Row, column=Column + 1, padx=5, pady=5)

class Output_Label:
    def __init__(self, master, text, Row, Column):
        # self.label
        self.label = Label(master, text=text)
        self.label.grid(row=Row, column=Column)
        self.label_text = StringVar()
        self.label_text.set('')
        self.label_result= Entry(master, text=self.label_text)
        self.label_result.grid(row=Row + 1, column=Column)
        

class Lamination_Output:
    def __init__(self, master, lamination_order, Row, Column):
        self.Lamination = Output_Label(master, f'Lamination-{lamination_order}', Row, Column)
        self.areaProduct = Output_Label(master, 'Area Product cm²', Row, Column +1)
        self.stackLamination = Output_Label(master, 'Stack mm', Row, Column + 2)
        self.tongueLamination = Output_Label(master, 'Tognue mm', Row, Column + 3)
        self.costLamination = Output_Label(master, 'Cost Rs', Row + 2, Column + 3)
        self.cuTempLamination = Output_Label(
            master,
            'Cu Temperature Rise',
            Row+2,
            Column+1
        )
        self.feTempLamination = Output_Label(
            master,
            'Fe Temperature Rise',
            Row + 2,
            Column + 2
        )
        self.coreLossLamination = Input_Label(master, 'Core Loss', Row, Column + 4)
        self.cuLossLamination = Input_Label(master, 'Copper Loss', Row+2, Column + 4)
        

class Strip_Output:
    """
    To simplify the strip outputs table so that the we can simply create as many
    we need. Also it helps in shortening the code.
    """
    def __init__(self, master, strip_number, Row, cmd):
        self.strip_number = strip_number
        self.type = Output_Label(master, 'Type', Row, 0) 
        self.stackStrip = Output_Label(master, 'Stack mm', Row, 1)
        self.tongueStrip = Output_Label(master, 'Tongue mm', Row, 2)
        self.wlStrip = Output_Label(master, 'Winding Length mm', Row, 3)
        self.wwStrip = Output_Label(master, 'Winding Width mm', Row, 4)
        self.built = Output_Label(master, 'Total Built', Row, 5)
        self.cuTempStrip = Output_Label(master, 'Cu Temperature rise', Row, 6)
        self.feTempStrip = Output_Label(master, 'Fe Temperature rise', Row, 7)
        self.cost = Output_Label(master, 'Cost Rs', Row, 8)
        # data button for strip output

        
        self.data = Button(master, text="Data", command=self.disableButton)
        self.data.grid(row=Row, column=10)

    def disableButton(self):
        data = pd.read_csv('/home/yash7/Desktop/EMD/auto-transformer/FINAL/results.csv')
        # if n = 1  i.e, strip_number 1
        n = self.strip_number - 1
        # now n = 0 then it can be applied to data[n : n+ 1] => data[0:1]
        data = data[n:n+1]
        print(data.columns)
        popup = Tk()
        popup.title(f'Data of {self.strip_number}')
        # popup.grab_set()
        primary_wire = Input_Label(popup, 'Primary wire', 0, 4)
        width_primary = Input_Label(popup, 'Primary width', 1, 4)
        height_primary = Input_Label(popup, 'Primary height', 2, 4)
        GetData(primary_wire, data['Primary wire'].min())
        GetData(width_primary, data['width primary'].min())
        GetData(height_primary, data['height primary'].min())
        secondary_wire = Input_Label(popup, 'Secondary', 0, 6)
        width_secondary = Input_Label(popup, 'Secondary width', 1, 6)
        height_secondary = Input_Label(popup, 'Secondary height', 2, 6)
        GetData(secondary_wire, data['Secondary wire'].min())
        GetData(width_secondary, data['width secondary'].min())
        GetData(height_secondary, data['height secondary'].min())

        # currents
        Row = 10
        # primary_current = Input_Label(popup, 'Primary current', Row, 3)
        # primary_voltage = Input_Label(popup, 'Primary voltage', Row, 5)
        # primary_power = Input_Label(popup, 'Primary Power', Row, 7)

        # secondary_current = Input_Label(popup, 'Srimary current', Row + 1, 3)
        # secondary_voltage = Input_Label(popup, 'Srimary voltage', Row + 1, 5)
        # secondary_power = Input_Label(popup, 'Srimary Power', Row + 1, 7)
        # print(data[n: n+1])
        print(data['Cost'])
        pass 

class GetData:
    def __init__(self, parameter, data):
        parameter.label_result.delete(0, END)
        parameter.label_result.insert(0, f'{data}')

class GetParameterData:
    def __init__(self, stripArray, ParameterColumn):
        """
        StripArray: [self.strip_I, self.strip_II]
        ParameterColumn is the required column of our result data
        Eg: results['Cost'], results['Stack mm']

        parameter: It is the proporty of Strip_Output class
        Strip_Output = ['type', 'stackStrip', 'tongueStrip', 'wwStrip',
            'cuTempStrip', 'feTempStrip', 'cost']
        """
        parameter = []
        n = 0
        for strip in stripArray:
            parameter.append(ParameterColumn[0+n:1+n].min())
            strip.label_result.delete(0, END)
            strip.label_result.insert(0, f'{parameter[n]}')
            n = n+1

class GetTypeData:
    def __init__(self, stripArray, ParameterRow):
        """
        StripArray: [self.strip_I, self.strip_II]

        ParameterRow: It is row of the results Dataframe with one row selected
        eg: [ 'results[0:1]', 'results[1:2]', 'results[2:3]' ]
        """
        type = ParameterRow['Type'].min()
        stripArray.type.label_result.delete(0, END)
        stripArray.type.label_result.insert(0, f'{type}')

        stack = ParameterRow['Stack mm'].min()
        stripArray.stackStrip.label_result.delete(0, END)
        stripArray.stackStrip.label_result.insert(0, f'{stack}')

        tongue = ParameterRow['Tongue mm'].min()
        stripArray.tongueStrip.label_result.delete(0, END)
        stripArray.tongueStrip.label_result.insert(0, f'{tongue}')

        ww = ParameterRow['ww mm'].min()
        stripArray.wwStrip.label_result.delete(0, END)
        stripArray.wwStrip.label_result.insert(0, f'{ww}')

        wl = ParameterRow['wl mm'].min()
        stripArray.wlStrip.label_result.delete(0, END)
        stripArray.wlStrip.label_result.insert(0, f'{wl}')

        cu = ParameterRow['Temperature rise Cu'].min()
        cu = round(cu, 3)
        stripArray.cuTempStrip.label_result.delete(0, END)
        stripArray.cuTempStrip.label_result.insert(0, f'{cu}')

        fe = ParameterRow['Temperature rise Fe'].min()
        fe = round(fe, 3)
        stripArray.feTempStrip.label_result.delete(0, END)
        stripArray.feTempStrip.label_result.insert(0, f'{fe}')

        cost = ParameterRow['Cost'].min()
        cost = round(cost , 2)
        stripArray.cost.label_result.delete(0, END)
        stripArray.cost.label_result.insert(0, f'{cost}') 

        built = ParameterRow['Total Built'].min()
        stripArray.built.label_result.delete(0, END)
        stripArray.built.label_result.insert(0, f'{built}')

class GetDataToLabel:
    def __init__(self, location, data):
        location.label_result.delete(0, END)
        location.label_result.insert(0, f'{data}')
        

root = Tk()
my_gui = StripGUI(root)
root.mainloop()