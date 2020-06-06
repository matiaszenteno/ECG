import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# initialize parameters
N = 20000000
p = 0.3
alpha = 0.3
beta = 60
tp = 56
tq = 21

# simulation range
simulation_time = 120

# variables
total_infected = { 'critic': 0, 'non_critic': 0 }
total_recovered = { 'critic': 0, 'non_critic': 0 }

def infections(N,alpha,beta,p,t):
    critics = np.floor(np.float_power(10,-5) * p * N * np.float_power(t,alpha) * np.exp(-t/beta))
    non_critics = np.floor(np.float_power(10,-5) * (1-p) * N * np.float_power(t,alpha) * np.exp(-t/beta))
    return critics, non_critics

def recoveries(N,alpha,beta,p,tp,tq,t):
    critics = np.floor(np.float_power(10,-5) * p * N * np.float_power(t-tp,alpha) * np.exp(-(t-tp)/beta)) if t >= tp else 0 
    non_critics = np.floor(np.float_power(10,-5) * (1-p) * N * np.float_power(t-tq,alpha) * np.exp(-(t-tq)/beta)) if t >= tq else 0 
    return critics, non_critics

def simulate():
    for t in range(simulation_time + 1):
        critic_infected, non_critic_infected = infections(N,alpha,beta,p,t)
        critic_recovered, non_critic_recovered = recoveries(N,alpha,beta,p,tp,tq,t)

        total_infected['critic'] = total_infected['critic'] + critic_infected
        total_infected['non_critic'] = total_infected['non_critic'] + non_critic_infected
        total_recovered['critic'] = total_recovered['critic'] + critic_recovered
        total_recovered['non_critic'] = total_recovered['non_critic'] + non_critic_recovered

        infected = critic_infected + non_critic_infected
        recovered = critic_recovered + non_critic_recovered
        actives = sum(total_infected.values()) - sum(total_recovered.values())

        print(f"DAY: {t} || Infectados: {infected} || Recuperados: {recovered} || Activos: {actives}")

screen = Screen()
screen.setworldcoordinates(0, 0, 120, 20000)

emily = Turtle(visible=False)
emily.forward(1)
emily.penup()

for t in range(simulation_time + 1):

        critic_infected, non_critic_infected = infections(N,alpha,beta,p,t)
        critic_recovered, non_critic_recovered = recoveries(N,alpha,beta,p,tp,tq,t)

        total_infected['critic'] = total_infected['critic'] + critic_infected
        total_infected['non_critic'] = total_infected['non_critic'] + non_critic_infected
        total_recovered['critic'] = total_recovered['critic'] + critic_recovered
        total_recovered['non_critic'] = total_recovered['non_critic'] + non_critic_recovered

        infected = critic_infected + non_critic_infected
        recovered = critic_recovered + non_critic_recovered
        actives = sum(total_infected.values()) - sum(total_recovered.values())

        y = actives
        emily.goto(t / 1, y)
        emily.pendown()

        print(f"DAY: {t} || Infectados: {infected} || Recuperados: {recovered} || Activos: {actives}")

screen.exitonclick()