from __future__ import division
from pyomo.environ import *
from coopr.pyomo import *
from copy import deepcopy 
import numpy as np
import pandas as pd

def solver_model(alpha, beta, gamma, limit_period):

    model = AbstractModel()

    # Interval t
    model.T = RangeSet(0,17)

    # Parameters
    model.d = Param(model.T)

    # Variables s, b, x, y
    model.s = Var(model.T, domain=NonNegativeReals)
    model.b = Var(model.T, domain=NonNegativeReals)
    model.x = Var(model.T, domain=NonNegativeReals)
    model.y = Var(model.T, domain=NonNegativeReals)

    # Load data from csv
    data = DataPortal(model=model)
    data.load(filename="simulation_total_per_week.csv", select=('Semana','Ventiladores requeridos'), param=model.d)

    def obj_expression(model):
        #return summation(model.s, model.x) + summation(model.b, model.y)
        return summation(model.x) + summation(model.y)

    model.OBJ = Objective(rule=obj_expression, sense=minimize)

    def purchase_cost_constraint(model, T):
        return model.s[T] == gamma * alpha * np.exp((-1 * beta * T)/2790)

    def inventory_cost_constraint(model, T):
        return model.b[T] == (1/gamma) * (1/alpha) * np.exp((beta * T)/2790)

    def inventory_constraint(model, T):
        if T:
            return model.x[T] + model.y[T-1] == model.d[T] + model.y[T]
        else:
            return model.x[T] == model.d[T] + model.y[T]

    def initial_inventory_constraint(model):
        return model.y[0] == 0

    # The next line creates constraints
    model.PurchaseCostConstraint = Constraint(model.T, rule=purchase_cost_constraint)
    model.InventoryCostConstraint = Constraint(model.T, rule=inventory_cost_constraint)
    model.InventoryConstraint = Constraint(model.T, rule=inventory_constraint)
    model.InitialInventoryConstraint = Constraint(rule=initial_inventory_constraint)

    instance = model.create_instance(data)
    instance.pprint()

    opt = SolverFactory('glpk')
    opt.solve(instance) 
    
    #### Write data
    # Print values for each variable explicitly
    #
    print("Print values for each variable explicitly")
    for i in model.x:
        print (str(model.x[i]), model.x[i].value)
    for i in model.y:
        print (str(model.y[i]), model.y[i].value)
        print("")

    #
    # Print values for all variables
    #
    print("Print values for all variables")
    for v in model.component_data_objects(Var):
        print (str(v), v.value)

if __name__ == "__main__":
    solver_model(1, 1, 1, 1)