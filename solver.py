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

    # Parameters
    model.s = Param(model.T)
    model.b = Param(model.T)
    model.d = Param(model.T)

    # Variables s, b, x, y
    model.x = Var(model.T, domain=NonNegativeReals)
    model.y = Var(model.T, domain=NonNegativeReals)

    # Load data from csv
    data = DataPortal(model=model)
    data.load(filename="simulation_"+city+"_per_week.csv", select=('Semana','Costo compra'), param=model.b)
    data.load(filename="simulation_"+city+"_per_week.csv", select=('Semana','Costo inventario'), param=model.s)
    data.load(filename="simulation_"+city+"_per_week.csv", select=('Semana','Ventiladores requeridos'), param=model.d)

    def obj_expression(model):
        #return summation(model.s, model.x) + summation(model.b, model.y)
        return summation(model.b, model.x) + summation(model.s, model.y)

    model.OBJ = Objective(rule=obj_expression, sense=minimize)

    def inventory_constraint(model, T):
        if T:
            return model.x[T] + model.y[T-1] == model.d[T] + model.y[T]
        else:
            return model.x[T] == model.d[T] + model.y[T]

    def initial_inventory_constraint(model):
        return model.y[0] == 0

    # The next line creates constraints
    model.InventoryConstraint = Constraint(model.T, rule=inventory_constraint)
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
    df_var_y = pd.DataFrame(vars_values[1], columns=['Var y'])

    df = pd.concat([
        pd.read_csv('simulation_'+city+'_per_week.csv')
    ])

    df_purchase_cost_per_week = df['Costo compra'].to_frame()
    df_inventory_cost_per_week = df['Costo inventario'].to_frame()

    df_purchase = df_var_x.mul(df_purchase_cost_per_week.values)
    df_purchase.columns = ['Costos compra']
    df_purchase.index.names = ['Semana']

    df_inventory = df_var_y.mul(df_inventory_cost_per_week.values)
    df_inventory.columns = ['Costos inventario']
    df_inventory.index.names = ['Semana']

    df_final = pd.concat([df_var_x.stack(), df_var_y.stack(), df_purchase.stack(), df_inventory.stack()], axis=0).unstack()
    df_final.to_csv('solved_'+city+'.csv')

if __name__ == "__main__":
    solver_model(1, 1, 1, 1)