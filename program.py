import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Label
from simulation import simulate, summary
from graph import plot_graph
from cases_table import CasesTableApp
from costs_table import CostsTableApp

class Display():
    def __init__(self):
        self.root = Tk()
        self.root.title('Coronavirus Software')
        self.root.geometry("400x400")

        self.root.grid_columnconfigure((0, 1, 2), weight=1)

        self.showSimulateOptionsButton = Button(self.root,
                          text = 'Simular nuevo',
                          command=lambda: self.show_simulation_buttons())
        
        self.splitLabel1 = Label(self.root, text = '----------------------------------')
        self.splitLabel2 = Label(self.root, text = '----------------')
        self.targetCasesNameLabel = Label(self.root, text = '')

        self.simulateVentilatorOneButton = Button(self.root,
                          text = 'Simular Ventilador GTX1060 PLUS (BARATO)',
                          command=lambda: self.simulate(1))
        self.simulateVentilatorTwoButton = Button(self.root,
                          text = 'Simular Ventilador HAMILTTONE-A1 (MEDIO)',
                          command=lambda: self.simulate(2))
        self.simulateVentilatorTreeButton = Button(self.root,
                          text = 'Simular Ventilador INIFINITY W4R (CARO)',
                          command=lambda: self.simulate(3))

        self.showGraphButton = Button(self.root,
                          text = 'Ver gráfico',
                          command=lambda: self.graph())

        self.casesSummaryButton = Button(self.root,
                          text = 'Ver resumen de casos por semana',
                          command=lambda: self.show_cases_table())

        self.costsSummaryButton = Button(self.root,
                          text = 'Ver resumen de ventiladores y costos',
                          command=lambda: self.show_costs_table())

        self.showSimulateOptionsButton.grid(row = 0, column = 1)
        self.splitLabel1.grid(row = 1, column = 1)

        self.root.mainloop()

    def show_simulation_buttons(self):
        self.showSimulateOptionsButton.grid_remove()
        self.showGraphButton.grid_remove()
        self.casesSummaryButton.grid_remove()
        self.costsSummaryButton.grid_remove()
        self.splitLabel1.grid_remove()

        self.simulateVentilatorOneButton.grid(row = 0, column = 1)
        self.simulateVentilatorTwoButton.grid(row = 1, column = 1)
        self.simulateVentilatorTreeButton.grid(row = 2, column = 1)
        self.splitLabel1.grid(row = 3, column = 1)

    def simulate(self, ventilator):

        simulate(ventilator)

        self.simulateVentilatorOneButton.grid_remove()
        self.simulateVentilatorTwoButton.grid_remove()
        self.simulateVentilatorTreeButton.grid_remove()

        self.showSimulateOptionsButton.grid(row = 0, column = 1)
        self.splitLabel1.grid(row = 1, column = 1)

        self.showGraphButton.grid(row = 2, column = 1)

        self.casesSummaryButton.grid(row = 3, column = 1)
        self.costsSummaryButton.grid(row = 4, column = 1)

    def graph(self):
        plot_graph()

    def show_cases_table(self):
        CasesTableApp()

    def show_costs_table(self):
        CostsTableApp()

    def quit(self):
        self.root.destroy()

if __name__ == "__main__":
    app = Display()
