# abstract1.py
from __future__ import division
from pyomo.environ import *

model = AbstractModel()

# Intervalo t
model.t = Param(within=NonNegativeIntegers)
model.T = RangeSet(1, model.t)

# Parámetros
model.s = Param(model.T)
model.b = Param(model.T)
model.d = Param(model.T)

# Variables x, y
model.x = Var(model.T, domain=NonNegativeReals)
model.y = Var(model.T, domain=NonNegativeReals)

def obj_expression(model):
    return summation(model.s, model.x) + summation(model.b, model.y)

model.OBJ = Objective(rule=obj_expression, sense=minimize)

def inventory_constraint(model, T):
    return model.x[T] + model.y[T-1] == model.d[T] + model.y[T]

def initial_inventory_constraint(model):
    return model.y[0] == 0

# the next line creates one constraint for each member of the set model.I
model.InventoryConstraint = Constraint(model.T, rule=inventory_constraint)