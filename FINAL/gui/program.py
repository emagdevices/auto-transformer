import tkinter as tk 

class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text = 'Input Voltage', width = 25, command = self.new_window)
        self.button1.pack()
        self.frame.pack()
    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)

class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
    def close_windows(self):
        self.master.destroy()

def main(): 
    root = tk.Tk()
    app = Demo1(root)
    root.mainloop()

if __name__ == '__main__':
    main()


input_Voltage_lable = Label(app, text='Input voltage (Vin))')
input_Voltage_lable.grid(row=0, column=0, padx=5, pady=5, sticky=E)

Input_Voltage_text = StringVar()
Input_Voltage_text.set('')
input_Voltage_box = Entry(app, textvariable=Input_Voltage_text)
input_Voltage_box.grid(row=0, column=1, padx=5, pady=5)