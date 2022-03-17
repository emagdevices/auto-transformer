from tkinter import *
import pandas as pd 

def task():
    current_required = float(Itext.get())
    J_required = float(Jtext.get())
    Area_required = current_required / J_required
    Area_required = Area_required * 100 # to convernt sqcm to sqmm

    # Uploading Swg table for reference values 
    swg_data = pd.read_csv('EMD - Sheet1.csv')
    
    required_swg = swg_data.iloc[(swg_data['Normal Conductor Area mm²'] - Area_required).abs().argsort()[:1]]
    # print('SWG '+ required_swg['SWG'].to_string(index=False))
    swg_final = required_swg['SWG'].to_string(index=False)
    label_swg_result.delete(0, END)
    label_swg_result.insert(0, f"{swg_final}")

    selected_swg = required_swg['SWG'].to_string(index=False)
    Area_of_selected_swg = required_swg['Normal Conductor Area mm²'].to_string(index=False)
    # print('Normal Conductor Area of selected SWG : ' + Area_of_selected_swg + ' mm²')
    label_Area_result.delete(0, END)
    label_Area_result.insert(0, f"{Area_of_selected_swg} mm²")



import tkinter as tk 

app = tk.Tk()
app.title("SWG identifier")

current_lable = Label(app, text='Current Required (I)')
current_lable.grid(row=0, column=0, padx=5, pady=5, sticky=E)

J_label = Label(app, text="Current Density required (J)")
J_label.grid(row=1, column=0, padx=5, pady=5, sticky=E)


Itext = StringVar()
Itext.set('')
current_box = Entry(app, textvariable=Itext)
current_box.grid(row=0, column=1, padx=5, pady=5)

Jtext = StringVar()
Jtext.set('')
J_box = Entry(app, textvariable=Jtext)
J_box.grid(row=1, column=1, padx=5, pady=5)

# 'Go' Button for getting the results
AgoButton = Button(app, text='Go', command=task)
AgoButton.grid(row=1, column=2, padx=5, pady=5)

# label for for writing the swg version
SWG_lable = Label(app, text="SWG version :")
SWG_lable.grid(row=2, column=0, padx=5, pady=5, sticky=E)

# label for writing the Normal Area for SWG
Final_Area = Label(app, text="Normal Area for SWG")
Final_Area.grid(row=3, column=0, padx=5, pady=5, sticky=E)

# for inseting the our result in the box of area box
lblAtext = StringVar()
lblAtext.set('')
label_Area_result = Entry(app, text=lblAtext)
label_Area_result.grid(row=3, column=1, padx=5, pady=5, sticky=E)

lblswgtext = StringVar()
lblswgtext.set('')
label_swg_result = Entry(app, text=lblswgtext)
label_swg_result.grid(row=2, column=1, padx=5, pady=5, sticky=E)

app.mainloop()
