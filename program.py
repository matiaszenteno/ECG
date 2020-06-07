import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Button
from simulation import simulate, summary
from table import ExampleApp

root = Tk()
root.title('Coronavirus Software')
root.geometry("400x200")

def graph():
	simulate()

def show_summary():
    curico_weeks_data, linares_weeks_data, talca_weeks_data = summary()

    app = ExampleApp(curico_weeks_data, linares_weeks_data, talca_weeks_data)
    app.mainloop()

graph_button = Button(root, text="Simulate it!", command=graph)
graph_button.pack()
show_summary_button = Button(root, text="Get summary!", command=show_summary)
show_summary_button.pack()

root.mainloop()