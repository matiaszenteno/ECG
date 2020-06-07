import random
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count

def animate(i, fig, ax, day_values, curico_cum_actives_values, linares_cum_actives_values, talca_cum_actives_values, data_curico, data_linares, data_talca):

    row_curico = next(data_curico)
    row_linares = next(data_linares)
    row_talca = next(data_talca)
    day = row_curico["Día"]

    curico_cum_actives = row_curico["Activos totales"]
    linares_cum_actives = row_linares["Activos totales"]
    talca_cum_actives = row_talca["Activos totales"]

    day_values.append(day)
    curico_cum_actives_values.append(curico_cum_actives)
    linares_cum_actives_values.append(linares_cum_actives)
    talca_cum_actives_values.append(talca_cum_actives)

    print(curico_cum_actives,'CURICO')
    print(linares_cum_actives,'LINARES')
    print(talca_cum_actives,'TALCA')

    plt.plot(day_values, curico_cum_actives_values)
    plt.plot(day_values, linares_cum_actives_values)
    plt.plot(day_values, talca_cum_actives_values)

    ax.legend(["Curicó ","Talca", "Linares"])
    ax.set_xlabel("Día")
    ax.set_ylabel("Casos activos")
    plt.title('Simulación')

def plot_graph():
    day_values = []
    curico_cum_actives_values = []
    linares_cum_actives_values = []
    talca_cum_actives_values = []

    csv_file_curico = open( 'simulation_Curicó.csv', 'r') 
    csv_file_linares = open( 'simulation_Linares.csv', 'r')   
    csv_file_talca = open( 'simulation_Talca.csv', 'r')        
    data_curico = csv.DictReader(csv_file_curico, delimiter = ',')
    data_linares = csv.DictReader(csv_file_linares, delimiter = ',')        
    data_talca = csv.DictReader(csv_file_talca, delimiter = ',')

    fig, ax = plt.subplots()
    ani = FuncAnimation(plt.gcf(), animate, frames=120, repeat=False, fargs=(fig, ax, day_values, curico_cum_actives_values, linares_cum_actives_values, talca_cum_actives_values, data_curico, data_linares, data_talca), interval=10)
    plt.tight_layout()
    plt.show()

