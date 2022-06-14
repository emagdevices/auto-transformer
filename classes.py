from tkinter import *
import pandas as pd

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
        