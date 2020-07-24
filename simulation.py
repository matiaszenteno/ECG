import pandas as pd
import numpy as np
import csv
from solver import solver_model

# Initialize parameters
Locations = [{'name': 'Curicó', 'population': '102710'},
             {'name': 'Linares', 'population': '88422'},
             {'name': 'Talca', 'population': '203873'}]
p = 0.3
alpha = 1.3
beta = 60
gamma_values = [4, 5, 6]
tp_values = [56, 42, 28]
tq = 21

# Simulation range
simulation_time = 120

def open_book(name):
    f = open(name, "w")

    # Column names
    fnames = ['Dia',
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

# Return infections in a specific day
def infections(N,alpha,beta,p,t):

    critics = np.floor(np.float_power(10,-5) * p * N 
                * np.float_power(t,alpha) 
                * np.exp(-t/beta))
    non_critics = np.floor(np.float_power(10,-5) * (1-p) * N 
                * np.float_power(t,alpha) 
                * np.exp(-t/beta))
    return critics, non_critics

# Return recoveries in a specific day
def recoveries(N,alpha,beta,p,tp,tq,t):

    critics = np.floor(np.float_power(10,-5) * p * N 
                * np.float_power(t-tp,alpha) 
                * np.exp(-(t-tp)/beta)) if t >= tp else 0 
    non_critics = np.floor(np.float_power(10,-5) * (1-p) * N 
                * np.float_power(t-tq,alpha) 
                * np.exp(-(t-tq)/beta)) if t >= tq else 0 
    return critics, non_critics

# Simulate in a range of days
def simulate(ventilator):
    gamma = gamma_values[ventilator - 1]
    tp = tp_values[ventilator - 1]

    for city in Locations:

        # Cumulative Variables
        cum_infected = { 'critic': 0, 'non_critic': 0 }
        cum_recovered = { 'critic': 0, 'non_critic': 0 }
        cum_actives = { 'critic': 0, 'non_critic': 0 }

        book , f = open_book(f"simulation_{city['name']}.csv")
        N = int(city['population'])

        # Iterate over days
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

            # Write info in csv
            book.writerow({
                'Dia': t,
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

    summary(gamma)

# Group simulation stats by weeks
def summary(gamma):
    # Read csv
    curico_data = pd.read_csv('simulation_Curicó.csv', encoding='iso-8859-1')
    linares_data = pd.read_csv('simulation_Linares.csv', encoding='iso-8859-1')
    talca_data = pd.read_csv('simulation_Talca.csv', encoding='iso-8859-1')

    ### First city ###
    curico_weeks_cum_data = curico_data.groupby(
                    curico_data.index // 7).agg(**{
                        'Dia': ('Dia', 'sum'),
                        'Nuevos infectados': ('Nuevos infectados', 'sum'),
                        'Nuevos infectados criticos': ('Nuevos infectados criticos', 'sum') ,
                        'Nuevos infectados no criticos': ('Nuevos infectados no criticos', 'sum'),
                        'Nuevos recuperados': ('Nuevos recuperados', 'sum'),
                        'Nuevos recuperados criticos': ('Nuevos recuperados criticos', 'sum'),
                        'Nuevos recuperados no criticos': ( 'Nuevos recuperados no criticos', 'sum'),
                        'Casos totales': ('Casos totales', 'sum'),
                        'Casos criticos totales': ('Casos criticos totales', 'sum'),
                        'Casos no criticos totales': ('Casos no criticos totales', 'sum'),
                        'Recuperados totales': ( 'Recuperados totales', 'sum'),
                        'Recuperados criticos totales': ('Recuperados criticos totales', 'sum'),
                        'Recuperados no criticos totales': ('Recuperados no criticos totales', 'sum'),
                        'Activos totales': ('Activos totales', 'sum'),
                        'Activos criticos totales': ( 'Activos criticos totales', 'sum'),
                        'Activos no criticos totales': ('Activos no criticos totales', 'sum'),
                        'Maximo activos criticos acumulado': ('Activos criticos totales', 'max'),
                    })

    # Rename index
    curico_weeks_cum_data.index.names = ['Semana']

    # Calculate required ventilators
    curico_weeks_cum_data['Ventiladores requeridos'] = (
            curico_weeks_cum_data['Maximo activos criticos acumulado'] 
            - curico_weeks_cum_data['Maximo activos criticos acumulado'].shift().fillna(0)).clip(lower=0)

    # Calculate purchase and inventory costs
    curico_weeks_cum_data['Costo inventario'] = gamma * alpha * np.exp((-1 * beta * (curico_weeks_cum_data.index*7))/2790)
    curico_weeks_cum_data['Costo compra'] = (1/gamma) * (1/alpha) * np.exp((beta * (curico_weeks_cum_data.index*7))/2790)

    # Drop unnecessary columns
    curico_weeks_cum_data.drop(['Dia', 'Maximo activos criticos acumulado'], axis=1, inplace=True)

    ### Second city ###
    linares_weeks_cum_data = linares_data.groupby(
                    linares_data.index // 7).agg(**{
                        'Dia': ('Dia', 'sum'),
                        'Nuevos infectados': ('Nuevos infectados', 'sum'),
                        'Nuevos infectados criticos': ('Nuevos infectados criticos', 'sum') ,
                        'Nuevos infectados no criticos': ('Nuevos infectados no criticos', 'sum'),
                        'Nuevos recuperados': ('Nuevos recuperados', 'sum'),
                        'Nuevos recuperados criticos': ('Nuevos recuperados criticos', 'sum'),
                        'Nuevos recuperados no criticos': ( 'Nuevos recuperados no criticos', 'sum'),
                        'Casos totales': ('Casos totales', 'sum'),
                        'Casos criticos totales': ('Casos criticos totales', 'sum'),
                        'Casos no criticos totales': ('Casos no criticos totales', 'sum'),
                        'Recuperados totales': ( 'Recuperados totales', 'sum'),
                        'Recuperados criticos totales': ('Recuperados criticos totales', 'sum'),
                        'Recuperados no criticos totales': ('Recuperados no criticos totales', 'sum'),
                        'Activos totales': ('Activos totales', 'sum'),
                        'Activos criticos totales': ( 'Activos criticos totales', 'sum'),
                        'Activos no criticos totales': ('Activos no criticos totales', 'sum'),
                        'Maximo activos criticos acumulado': ('Activos criticos totales', 'max'),
                    })

    # Rename index
    linares_weeks_cum_data.index.names = ['Semana']

    # Calculate required ventilators
    linares_weeks_cum_data['Ventiladores requeridos'] = (
            linares_weeks_cum_data['Maximo activos criticos acumulado'] 
            - linares_weeks_cum_data['Maximo activos criticos acumulado'].shift().fillna(0)).clip(lower=0)

    # Calculate purchase and inventory costs
    linares_weeks_cum_data['Costo inventario'] = gamma * alpha * np.exp((-1 * beta * (linares_weeks_cum_data.index*7))/2790)
    linares_weeks_cum_data['Costo compra'] = (1/gamma) * (1/alpha) * np.exp((beta * (linares_weeks_cum_data.index*7))/2790)

    # Drop unnecessary columns
    linares_weeks_cum_data.drop(['Dia', 'Maximo activos criticos acumulado'], axis=1, inplace=True)

    ### Third city ###
    talca_weeks_cum_data = talca_data.groupby(
                    talca_data.index // 7).agg(**{
                        'Dia': ('Dia', 'sum'),
                        'Nuevos infectados': ('Nuevos infectados', 'sum'),
                        'Nuevos infectados criticos': ('Nuevos infectados criticos', 'sum') ,
                        'Nuevos infectados no criticos': ('Nuevos infectados no criticos', 'sum'),
                        'Nuevos recuperados': ('Nuevos recuperados', 'sum'),
                        'Nuevos recuperados criticos': ('Nuevos recuperados criticos', 'sum'),
                        'Nuevos recuperados no criticos': ( 'Nuevos recuperados no criticos', 'sum'),
                        'Casos totales': ('Casos totales', 'sum'),
                        'Casos criticos totales': ('Casos criticos totales', 'sum'),
                        'Casos no criticos totales': ('Casos no criticos totales', 'sum'),
                        'Recuperados totales': ( 'Recuperados totales', 'sum'),
                        'Recuperados criticos totales': ('Recuperados criticos totales', 'sum'),
                        'Recuperados no criticos totales': ('Recuperados no criticos totales', 'sum'),
                        'Activos totales': ('Activos totales', 'sum'),
                        'Activos criticos totales': ( 'Activos criticos totales', 'sum'),
                        'Activos no criticos totales': ('Activos no criticos totales', 'sum'),
                        'Maximo activos criticos acumulado': ('Activos criticos totales', 'max'),
                    })

    # Rename index
    talca_weeks_cum_data.index.names = ['Semana']

    # Calculate required ventilators
    talca_weeks_cum_data['Ventiladores requeridos'] = (
            talca_weeks_cum_data['Maximo activos criticos acumulado'] 
            - talca_weeks_cum_data['Maximo activos criticos acumulado'].shift().fillna(0)).clip(lower=0)

    # Calculate purchase and inventory costs
    talca_weeks_cum_data['Costo inventario'] = gamma * alpha * np.exp((-1 * beta * (talca_weeks_cum_data.index*7))/2790)
    talca_weeks_cum_data['Costo compra'] = (1/gamma) * (1/alpha) * np.exp((beta * (talca_weeks_cum_data.index*7))/2790)

    # Drop unnecessary columns
    talca_weeks_cum_data.drop(['Dia', 'Maximo activos criticos acumulado'], axis=1, inplace=True)


    # Write info in csv
    curico_weeks_cum_data.to_csv('simulation_Curicó_per_week.csv')
    linares_weeks_cum_data.to_csv('simulation_Linares_per_week.csv')
    talca_weeks_cum_data.to_csv('simulation_Talca_per_week.csv')

    merge_csv()

def merge_csv():
    df_per_day = pd.concat([
        pd.read_csv('simulation_Curicó.csv'),
        pd.read_csv('simulation_Linares.csv'),
        pd.read_csv('simulation_Talca.csv')
    ])

    df_per_week = pd.concat([
        pd.read_csv('simulation_Curicó_per_week.csv'),
        pd.read_csv('simulation_Linares_per_week.csv'),
        pd.read_csv('simulation_Talca_per_week.csv')
    ])

    result_per_day = df_per_day.groupby('Dia', as_index=False).sum()
    result_per_week = df_per_week.groupby(['Semana','Costo compra','Costo inventario'], as_index=False).sum()

    result_per_day.to_csv('simulation_total.csv', index=False)
    result_per_week.to_csv('simulation_total_per_week.csv', index=False)

    solver()

def solver():
    solver_model()

if __name__ == "__main__":
    simulate()