from __future__ import division
from pyomo.environ import *
from coopr.pyomo import *
from copy import deepcopy 
import numpy as np
import pandas as pd

def solver_model():
    cities = ["Curicó","Linares","Talca","total"]
    for city in cities:
        solver_city(city)

def solver_city(city):

    model = AbstractModel()

    # Interval t
    model.T = RangeSet(0,17)
    model.TDays = RangeSet(0,121)

    # Parameters
    model.sDays = Param(model.TDays)
    model.b = Param(model.T)
    model.d = Param(model.T)
    model.dDays = Param(model.TDays)

    # Variables s, b, x, y
    model.x = Var(model.T, domain=NonNegativeReals) # Ventilators purchase
    model.y = Var(model.T, domain=NonNegativeReals) # Over demand capacity per week
    model.z = Var(model.T, domain=NonNegativeReals) # Cumulative ventilators

    # Load data from csv
    data = DataPortal(model=model)
    data.load(filename="simulation_"+city+"_per_week.csv", select=('Semana','Costo compra'), param=model.b)
    data.load(filename="simulation_"+city+".csv", select=('Dia','Costo inventario'), param=model.sDays)
    data.load(filename="simulation_"+city+"_per_week.csv", select=('Semana','Ventiladores requeridos'), param=model.d)
    data.load(filename="simulation_"+city+".csv", select=('Dia','Activos criticos totales'), param=model.dDays)

    def obj_expression(model):
        #return summation(model.s, model.x) + summation(model.b, model.y)
        purchase_var_cost = summation(model.b, model.x)
        inventory_var_cost = 0

        for i in range (0,121):
            var_z = model.z[i // 7]
            inventory_var_cost += model.sDays[i] * (var_z - model.dDays[i])

        return purchase_var_cost + inventory_var_cost

    model.OBJ = Objective(rule=obj_expression, sense=minimize)

    def inventory_constraint(model, T):
        return model.z[T] == model.d[T] + model.y[T]

    def cumulative_ventilators_constraint(model, T):
        if T:
            return model.z[T] == model.z[T-1] + model.x[T]
        else:
            return model.z[T] == model.x[T]

    def initial_inventory_constraint(model):
        return model.y[0] == 0

    # The next line creates constraints
    model.InventoryConstraint = Constraint(model.T, rule=inventory_constraint)
    model.CumulativeVentilatorsConstraint = Constraint(model.T, rule=cumulative_ventilators_constraint)
    model.InitialInventoryConstraint = Constraint(rule=initial_inventory_constraint)

    instance = model.create_instance(data)
    instance.pprint()

    opt = SolverFactory('glpk')
    results = opt.solve(instance, tee=True)
    results.write()
    instance.solutions.load_from(results)

    # Set var values
    vars_values = []
    for v in instance.component_objects(Var, active=True):
        var_values = []
        print ("Variable",v)
        varobject = getattr(instance, str(v))
        for index in varobject:
            var_values.append(varobject[index].value)
            print ("   ",index, varobject[index].value)
        vars_values.append(var_values)

    df_var_x = pd.DataFrame(vars_values[0], columns=['Var x']) 

    df_var_z = pd.DataFrame(vars_values[2], columns=['Var z'])
    df_var_z = pd.DataFrame(df_var_z.values.repeat(7, axis=0), columns=df_var_z.columns)
    df_var_z.drop(df_var_z.tail(5).index,inplace=True)

    df_per_week = pd.concat([
        pd.read_csv('simulation_'+city+'_per_week.csv')
    ])

    df = pd.concat([
        pd.read_csv('simulation_'+city+'.csv')
    ])

    df_purchase_cost_per_week = df_per_week['Costo compra'].to_frame()
    df_inventory_cost = df['Costo inventario'].to_frame()

    df_purchase = df_var_x.mul(df_purchase_cost_per_week.values)
    df_purchase.columns = ['Costos compra']
    df_purchase.index.names = ['Semana']

    df_inventory = (df_var_z['Var z'] - df['Activos criticos totales']).mul(df['Costo inventario']).to_frame()
    df_inventory.columns = ['Costos inventario']
    df_inventory.index.names = ['Dia']

    df_final_purchase = pd.concat([df_var_x.stack(), df_purchase.stack()], axis=0).unstack()
    df_final_purchase.to_csv('solved_purchase_costs_'+city+'.csv')

    df_inventory.to_csv('solved_inventory_costs_'+city+'.csv')

if __name__ == "__main__":
    solver_model(1, 1, 1, 1)