import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label
from simulation import simulate, summary
from table import TableApp

class Display():
    def __init__(self):
        self.root = Tk()
        self.root.title('Coronavirus Software')
        self.root.geometry("400x400")

        self.root.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.target_cases = None
        self.target_cases_name = None

        self.showSimulateOptionsButton = Button(self.root,
                          text = 'Simular',
                          command=lambda: self.show_simulation_buttons())
        
        self.splitLabel = Label(self.root, text = '-----------')
        self.targetCasesNameLabel = Label(self.root, text = '')

        self.simulateActivesCasesButton = Button(self.root,
                          text = 'Simular Casos Activos',
                          command=lambda: self.graph(1))   
        self.simulateTotalCasesButton = Button(self.root,
                          text = 'Simular Casos Totales',
                          command=lambda: self.graph(0))

        self.cumSummaryButton = Button(self.root,
                          text = 'Ver resumen de acumulados por semana',
                          command=lambda: self.show_summary("cum"))

        self.meanSummaryButton = Button(self.root,
                          text = 'Ver resumen de promedio diario por semana',
                          command=lambda: self.show_summary("mean"))

        self.showSimulateOptionsButton.grid(row = 0, column = 1)
        self.splitLabel.grid(row = 1, column = 1)

        self.root.mainloop()

    def show_simulation_buttons(self):
        self.showSimulateOptionsButton.grid_remove()

        self.simulateActivesCasesButton.grid(row = 0, column = 1)
        self.simulateTotalCasesButton.grid(row = 1, column = 1)
        self.splitLabel.grid(row = 2, column = 1)

    def graph(self, stat):
        self.target_cases = 1 if stat else 0
        self.target_cases_name = "Casos Activos" if stat else "Casos Totales"


        self.simulateActivesCasesButton.grid_remove()
        self.simulateTotalCasesButton.grid_remove()

        self.showSimulateOptionsButton.grid(row = 0, column = 1)
        self.splitLabel.grid(row = 1, column = 1)

        self.targetCasesNameLabel['text'] = "Datos en resumen a mostrar: " + self.target_cases_name
        self.targetCasesNameLabel.grid(row = 2, column = 1)

        self.cumSummaryButton.grid(row = 3, column = 1)
        self.meanSummaryButton.grid(row = 4, column = 1)

        simulate(stat)

    def show_summary(self, stat):
        data = summary()

        tableApp = TableApp(data[stat], self.target_cases)
        tableApp.mainloop()

    def quit(self):
        self.root.destroy()

if __name__ == "__main__":
    app = Display()
