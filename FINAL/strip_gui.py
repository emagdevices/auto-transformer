# from tkinter import StringVar, Tk, Label, Button, Entry
from tkinter import *
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
            'Regulation [Hz]',
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
                                    Output Labels
        ================================================================
        """


        """
        ================================================================
                                        Buttons
        ================================================================
        """
        self.strip_button = Button(master, text="Calculate Strip", command=self.strip)
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
        # output_power = 40000
        # input_voltage = 230
        # output_voltage = 230
        # efficiency = 99
        # regulation = 5
        # b_ac = 1.25
        # current_density = 300
        # Rate_of_Cu = 950
        # Rate_of_Fe = 250
        # standard constants

        Core_Loss_Factor = 1.5 
        bobbin_thickness = 1.5  # mm
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
        # try:
        final_result = final_result.sort_values('Cost') 

        print(final_result.sort_values('Cost'))
        # print(final_result)
        pass 


class Input_Label:
    def __init__(self, master, text, Row, Column):
        self.label = Label(master, text=text)
        self.label.grid(row=Row, column=Column)
        self.label_text = StringVar()
        self.label_text.set('')
        self.label_box = Entry(master, textvariable=self.label_text)
        self.label_box.grid(row=Row, column=Column + 1, padx=5, pady=5)

root = Tk()
my_gui = StripGUI(root)
root.mainloop()