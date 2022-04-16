from tkinter import *
import tkinter as tk 

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master=None)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid()

app = Application()
app.master.title('Sample application')
app.mainloop()
