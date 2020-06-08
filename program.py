import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Button
from simulation import simulate, summary
from table import TableApp

class Display():
    def __init__(self):
        self.root = Tk()
        self.root.title('Coronavirus Software')
        self.root.geometry("400x200")
        
        self.target_cases = None

        self.showSimulateOptionsButton = Button(self.root,
                          text = 'Simular',
                          command=lambda: self.show_simulation_buttons())
        self.simulateActivesCasesButton = Button(self.root,
                          text = 'Simular Casos Activos',
                          command=lambda: self.graph(1))   
        self.simulateTotalCasesButton = Button(self.root,
                          text = 'Simular Casos Totales',
                          command=lambda: self.graph(0))  
        self.cumSummaryButton = Button(self.root,
                          text = 'Ver resumen de activos acumulados por semana',
                          command=lambda: self.show_summary("cum"))   
        self.meanSummaryButton = Button(self.root,
                          text = 'Ver resumen de activos promedio diario por semana',
                          command=lambda: self.show_summary("mean"))       

        self.showSimulateOptionsButton.pack()
        self.root.mainloop()

    def show_simulation_buttons(self):
        self.cumSummaryButton.pack_forget()
        self.meanSummaryButton.pack_forget()

        self.simulateActivesCasesButton.pack()
        self.simulateTotalCasesButton.pack()

    def graph(self, stat):
        self.target_cases = 1 if stat else 0

        self.simulateActivesCasesButton.pack_forget()
        self.simulateTotalCasesButton.pack_forget()

        simulate(stat)

        self.cumSummaryButton.pack()
        self.meanSummaryButton.pack()

    def show_summary(self, stat):
        data = summary()

        tableApp = TableApp(data[stat], self.target_cases)
        tableApp.mainloop()

    def quit(self):
        self.root.destroy()

if __name__ == "__main__":
    app = Display()
