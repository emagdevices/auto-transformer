from tkinter import *

OPTIONS = [
"Copper",
"Aluminium"
] #etc

master = Tk()

conductor = StringVar(master)
conductor.set(OPTIONS[0]) # default value

w = OptionMenu(master, conductor, *OPTIONS)
w.pack()

def ok():
    if conductor.get() == "Copper":
        Resistivity_conductor = 1.68 * 10**-6 # ohm cm
    if conductor.get() == "Aluminium":
        Resistivity_conductor = 2.65 * 10**-6 # ohm cm
    return Resistivity_conductor



button = Button(master, text="OK", command=ok)
button.pack()

print (f"Resistivity value of {conductor.get()} : {ok()}")
# Conductor = [{material: "copper", Rate_of_Conductor: 950}]



mainloop()