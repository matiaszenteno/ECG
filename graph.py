import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(i, fig, ax, day_values, 
            cum_infected_values, 
            cum_recovered_values, 
            cum_actives_values, 
            data_total):
  
    row = next(data_total)
    day = row["Dia"]

    cum_infected = row["Casos totales"]
    cum_recovered = row["Recuperados totales"]
    cum_actives = row["Activos totales"]

    day_values.append(day)
    cum_infected_values.append(float(cum_infected))
    cum_recovered_values.append(float(cum_recovered))
    cum_actives_values.append(float(cum_actives))

    plt.plot(day_values, cum_infected_values, color="green")
    plt.plot(day_values, cum_recovered_values, color="red")
    plt.plot(day_values, cum_actives_values, color="blue")

    ax.legend(["Infectados totales", "Recuperados totales", "Activos totales"])
    ax.set_xlabel("Dia")
    plt.title('Simulación')

def plot_graph():
    
    csv_file = open('simulation_total.csv',)

    data_total = csv.DictReader(csv_file, delimiter = ',')
    
    day_values = []
    cum_infected_values = []
    cum_recovered_values = []
    cum_actives_values = []

    fig, ax = plt.subplots()
    ani = FuncAnimation(fig, animate, fargs=(fig, ax, day_values, 
                            cum_infected_values, 
                            cum_recovered_values, 
                            cum_actives_values, 
                            data_total), interval=60, frames=120, repeat=False)
    plt.tight_layout()
    plt.show()
