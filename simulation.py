import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

# Initialize Parameters
N = 20000000
p = 0.3
alpha = 0.3
beta = 60
tp = 28
tq = 21

# Simulation Range
simulation_time = 120

# Cumulative Variables
cum_infected = { 'critic': 0, 'non_critic': 0 }
cum_recovered = { 'critic': 0, 'non_critic': 0 }
cum_actives = { 'critic': 0, 'non_critic': 0 }

print(cum_infected["critic"])

def open_book():
    f = open("simulation_data.csv", "w")

    fnames = ['Nuevos infectados',
              'Nuevos infectados críticos',  
              'Nuevos infectados no críticos',
              'Nuevos recuperados',
              'Nuevos recuperados críticos',
              'Nuevos recuperados no críticos',
              'Casos totales',
              'Casos críticos totales',
              'Casos no críticos totales',
              'Recuperados totales',
              'Recuperados críticos totales',
              'Recuperados no críticos totales',
              'Activos totales',
              'Activos críticos totales',
              'Activos no críticos totales',
    ]

    writer = csv.DictWriter(f, fieldnames=fnames)
    writer.writeheader()

    return writer

def infections(N,alpha,beta,p,t):

    critics = np.floor(np.float_power(10,-5) * p * N * np.float_power(t,alpha) * np.exp(-t/beta))
    non_critics = np.floor(np.float_power(10,-5) * (1-p) * N * np.float_power(t,alpha) * np.exp(-t/beta))
    return critics, non_critics

def recoveries(N,alpha,beta,p,tp,tq,t):

    critics = np.floor(np.float_power(10,-5) * p * N * np.float_power(t-tp,alpha) * np.exp(-(t-tp)/beta)) if t >= tp else 0 
    non_critics = np.floor(np.float_power(10,-5) * (1-p) * N * np.float_power(t-tq,alpha) * np.exp(-(t-tq)/beta)) if t >= tq else 0 
    return critics, non_critics

def simulate(book):

    for t in range(simulation_time + 1):
        new_critic_infected, new_non_critic_infected = infections(N,alpha,beta,p,t)
        new_critic_recovered, new_non_critic_recovered = recoveries(N,alpha,beta,p,tp,tq,t)

        delta_critic_actives = new_critic_infected - new_critic_recovered
        delta_non_critic_actives = new_non_critic_infected - new_non_critic_recovered

        cum_infected["critic"] += new_critic_infected
        cum_infected["non_critic"] += new_non_critic_infected
        cum_recovered["critic"] += new_critic_recovered
        cum_recovered["non_critic"] += new_non_critic_recovered
        cum_actives["critic"] += delta_critic_actives
        cum_actives["non_critic"] += delta_non_critic_actives

        print(sum(cum_infected.values()))
        
        book.writerow({'Nuevos infectados': new_critic_infected + new_non_critic_infected,
                       'Nuevos infectados críticos': new_critic_infected,  
                       'Nuevos infectados no críticos': new_non_critic_infected,
                       'Nuevos recuperados': new_critic_recovered + new_non_critic_recovered,
                       'Nuevos recuperados críticos': new_critic_recovered, 
                       'Nuevos recuperados no críticos': new_non_critic_recovered, 
                       'Casos totales': sum(cum_infected.values()),
                       'Casos críticos totales': cum_infected["critic"],
                       'Casos no críticos totales': cum_infected["non_critic"],
                       'Recuperados totales': sum(cum_recovered.values()),
                       'Recuperados críticos totales': cum_recovered["critic"],
                       'Recuperados no críticos totales': cum_recovered["non_critic"],
                       'Activos totales': sum(cum_actives.values()),
                       'Activos críticos totales': cum_actives["critic"],
                       'Activos no críticos totales': cum_actives["non_critic"],

        })

if __name__ == "__main__":
    book = open_book()
    simulate(book)