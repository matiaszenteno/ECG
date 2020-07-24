from pyomo.environ import *
import pandas as pd

m = ConcreteModel()

m.s = Set(initialize=[1,2,3])
m.p = Param(initialize=1, mutable=True)
m.x = Var(m.s, bounds=(1,3))
m.obj = Objective(expr=m.p*sum(m.x[k] for k in m.s))

solver = SolverFactory('glpk')

all_data={}
for j in range(1,4):

    m.p = j
    solver.solve(m)

    data = {}

    for i in m.component_data_objects(Param):
        data[i.name] = value(i)
    for i in m.component_data_objects(Var):
        data[i.name] = value(i)
    for i in m.component_data_objects(Objective):
        data[i.name] = value(i)

    all_data['Solve '+str(j)] = pd.Series(data)

df = pd.DataFrame(all_data)
print(df)