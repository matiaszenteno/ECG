import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from graph import plot_graph

# Initialize Parameters
Locations = [{'name': 'Curicó', 'population': '102710'},
             {'name': 'Linares', 'population': '88422'},
             {'name': 'Talca', 'population': '203873'}]
p = 0.3
alpha = 1.3
beta = 60
tp = 56 # undefined
tq = 21

# Simulation Range
simulation_time = 120

def open_book(name):
    f = open(name, "w")

    fnames = ['Día',
              'Nuevos infectados',
              'Nuevos infectados criticos',  
              'Nuevos infectados no criticos',
              'Nuevos recuperados',
              'Nuevos recuperados criticos',
              'Nuevos recuperados no criticos',
              'Casos totales',
              'Casos criticos totales',
              'Casos no criticos totales',
              'Recuperados totales',
              'Recuperados criticos totales',
              'Recuperados no criticos totales',
              'Activos totales',
              'Activos criticos totales',
              'Activos no criticos totales',
    ]

    writer = csv.DictWriter(f, fieldnames=fnames)
    writer.writeheader()

    return writer, f

def infections(N,alpha,beta,p,t):

    critics = np.floor(np.float_power(10,-5) * p * N 
                * np.float_power(t,alpha) 
                * np.exp(-t/beta))
    non_critics = np.floor(np.float_power(10,-5) * (1-p) * N 
                * np.float_power(t,alpha) 
                * np.exp(-t/beta))
    return critics, non_critics

def recoveries(N,alpha,beta,p,tp,tq,t):

    critics = np.floor(np.float_power(10,-5) * p * N 
                * np.float_power(t-tp,alpha) 
                * np.exp(-(t-tp)/beta)) if t >= tp else 0 
    non_critics = np.floor(np.float_power(10,-5) * (1-p) * N 
                * np.float_power(t-tq,alpha) 
                * np.exp(-(t-tq)/beta)) if t >= tq else 0 
    return critics, non_critics

def simulate(stat):

    for city in Locations:

        # Cumulative Variables
        cum_infected = { 'critic': 0, 'non_critic': 0 }
        cum_recovered = { 'critic': 0, 'non_critic': 0 }
        cum_actives = { 'critic': 0, 'non_critic': 0 }

        book , f = open_book(f"simulation_{city['name']}.csv")
        N = int(city['population'])

        for t in range(simulation_time + 1):
            new_critic_infected, new_non_critic_infected = infections(
                                                        N,alpha,beta,p,t)
            
            new_critic_recovered, new_non_critic_recovered = recoveries(
                                                        N,alpha,beta,p,tp,tq,t)

            delta_critic_actives = (new_critic_infected 
                                    - new_critic_recovered)
            delta_non_critic_actives = (new_non_critic_infected 
                                        - new_non_critic_recovered)

            cum_infected["critic"] += new_critic_infected
            cum_infected["non_critic"] += new_non_critic_infected
            cum_recovered["critic"] += new_critic_recovered
            cum_recovered["non_critic"] += new_non_critic_recovered
            cum_actives["critic"] += delta_critic_actives
            cum_actives["non_critic"] += delta_non_critic_actives

            book.writerow({'Día': t,
                'Nuevos infectados': new_critic_infected 
                                     + new_non_critic_infected,
                'Nuevos infectados criticos': new_critic_infected,  
                'Nuevos infectados no criticos': new_non_critic_infected,
                'Nuevos recuperados': new_critic_recovered 
                                      + new_non_critic_recovered,
                'Nuevos recuperados criticos': new_critic_recovered, 
                'Nuevos recuperados no criticos': new_non_critic_recovered, 
                'Casos totales': sum(cum_infected.values()),
                'Casos criticos totales': cum_infected["critic"],
                'Casos no criticos totales': cum_infected["non_critic"],
                'Recuperados totales': sum(cum_recovered.values()),
                'Recuperados criticos totales': cum_recovered["critic"],
                'Recuperados no criticos totales': cum_recovered["non_critic"],
                'Activos totales': sum(cum_actives.values()),
                'Activos criticos totales': cum_actives["critic"],
                'Activos no criticos totales': cum_actives["non_critic"],
            })
        f.close()

    plot_graph(stat)

def summary():
    curico_data = pd.read_csv('simulation_Curicó.csv', encoding='iso-8859-1')
    linares_data = pd.read_csv('simulation_Linares.csv', encoding='iso-8859-1')
    talca_data = pd.read_csv('simulation_Talca.csv', encoding='iso-8859-1')

    curico_weeks_cum_data = curico_data.groupby(
                                        curico_data.index // 7).sum()
    linares_weeks_cum_data = linares_data.groupby(
                                        linares_data.index // 7).sum()
    talca_weeks_cum_data = talca_data.groupby(
                                        talca_data.index // 7).sum()

    curico_weeks_mean_data = curico_data.groupby(
                                        curico_data.index // 7).mean().round(2)
    linares_weeks_mean_data = linares_data.groupby(
                                        linares_data.index // 7).mean().round(2)
    talca_weeks_mean_data = talca_data.groupby(
                                        talca_data.index // 7).mean().round(2)

    result = {"cum":
                [curico_weeks_cum_data,
                talca_weeks_cum_data,
                linares_weeks_cum_data],
              "mean":
                [curico_weeks_mean_data,
                talca_weeks_mean_data,
                linares_weeks_mean_data]
    }

    return result

if __name__ == "__main__":
    simulate()