import random
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import pandas as pd

def animate(i, fig, ax, day_values, 
            curico_cum_actives_values, 
            linares_cum_actives_values, 
            talca_cum_actives_values, 
            data_curico, 
            data_linares, 
            data_talca,
            stat):
  
    row_curico = next(data_curico)
    row_linares = next(data_linares)
    row_talca = next(data_talca)
    day = row_curico["Día"]

    curico_cum_actives = row_curico["Activos totales" if stat else "Casos totales"]
    linares_cum_actives = row_linares["Activos totales" if stat else "Casos totales"]
    talca_cum_actives = row_talca["Activos totales" if stat else "Casos totales"]

    day_values.append(day)
    curico_cum_actives_values.append(float(curico_cum_actives))
    linares_cum_actives_values.append(float(linares_cum_actives))
    talca_cum_actives_values.append(float(talca_cum_actives))

    plt.plot(day_values, talca_cum_actives_values, color="green")
    plt.plot(day_values, curico_cum_actives_values, color="red")
    plt.plot(day_values, linares_cum_actives_values, color="blue")

    ax.legend(["Talca","Curicó ","Linares"])
    ax.set_xlabel("Día")
    ax.set_ylabel("Casos activos")
    plt.title('Simulación')

def plot_graph(stat):
    
    csv_file_curico = open('simulation_Curicó.csv',)
    csv_file_linares = open('simulation_Linares.csv',)  
    csv_file_talca = open('simulation_Talca.csv',)     

    data_curico = csv.DictReader(csv_file_curico, delimiter = ',')
    data_linares = csv.DictReader(csv_file_linares, delimiter = ',')        
    data_talca = csv.DictReader(csv_file_talca, delimiter = ',')
    
    day_values = []
    curico_cum_actives_values = []
    linares_cum_actives_values = []
    talca_cum_actives_values = []

    fig, ax = plt.subplots()
    ani = FuncAnimation(fig, animate, fargs=(fig, ax, day_values, 
                            curico_cum_actives_values, 
                            linares_cum_actives_values, 
                            talca_cum_actives_values, 
                            data_curico, 
                            data_linares, 
                            data_talca,
                            stat), interval=100, frames=120, repeat=False)
    plt.tight_layout()
    plt.show()
