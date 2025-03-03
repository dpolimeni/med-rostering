import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from collections import defaultdict

from constraints import *
from departments_data import ID_TO_WEEKDAY_NAME, SHIFT_NAMES

from get_monthly_data import get_monthly_data
from gurobipy import GRB, Model

date = input("Enter the date: ")
month = int(date.split("-")[1])
year = int(date.split("-")[0])
MAX_SHIFTS = 6
LOW_WORKING_DEPARTMENTS = ["reparto_ostetricia", "reparto_ginecologia"]
HIGH_WORKING_DEPARTMENTS = [
    "ambulatorio_ostetricia",
    "ambulatorio_ginecologia",
    "day_hospital_ostetricia",
    "sala_operatoria",
]

idx_dow, dow_idxs = get_monthly_data(date)
num_days = len(idx_dow)
doctors = {
    # reparto_ostetricia
    "alessia_berardi": "reparto_ostetricia",
    "anna_romano": "reparto_ostetricia",
    "virginia_magro": "reparto_ostetricia",
    # ambulatorio_ostetricia
    "gregorio_volpe": "ambulatorio_ostetricia",
    "alessia_antonacci": "ambulatorio_ostetricia",
    # day_hospital_ostetricia
    "lucrezia_lamorgese": "day_hospital_ostetricia",
    # reparto_ginecologia
    "antonio_de_palma": "reparto_ginecologia",
    "alessandra_ascani": "reparto_ginecologia",
    # ambulatorio_ginecologia
    "roberta_arseni": "ambulatorio_ginecologia",
    "marica_di_viesti": "ambulatorio_ginecologia",
    "simona_incamicia": "ambulatorio_ginecologia",
    "flavia_denaro": "ambulatorio_ginecologia",
    # sala_operatoria
    "lucia_oliva": "sala_operatoria",
}

dperartments_doctors = defaultdict(list)
for doctor, dep in doctors.items():
    dperartments_doctors[dep].append(doctor)


# Start Building constraints
model = Model("Shifts-Manager")
variables = model.addVars(
    list(doctors.keys()), list(range(num_days)), [0, 1], vtype=GRB.BINARY, name="x"
)
max_work_vars = model.addVars(
    list(dperartments_doctors.keys()), vtype=GRB.CONTINUOUS, name="max_work_vars"
)
min_work_vars = model.addVars(
    list(dperartments_doctors.keys()), vtype=GRB.CONTINUOUS, name="min_work_vars"
)
# max_worker_vars =

# Consecutive days constraint
build_consecutive_shift_constraint(
    model, variables, list(doctors.keys()), num_days, num_shifts=2, consecutive_limit=10
)

# Custom constraints None for now

# Min and Max shifts per doctor
build_doctors_per_shift_constraint(model, variables, num_days)

# Department constraints
for doctor, department in doctors.items():
    build_department_constraints(model, variables, department, doctor, dow_idxs)

# STRATEGY 1 contraints
build_shifts_range_contraints(
    model, variables, list(doctors.keys()), num_days, relaxation=3
)

for low_dep in LOW_WORKING_DEPARTMENTS:
    for high_dep in HIGH_WORKING_DEPARTMENTS:
        build_cross_department_constraint(
            model,
            variables,
            (low_dep, dperartments_doctors[low_dep]),
            (high_dep, dperartments_doctors[high_dep]),
        )

for doctor in doctors:
    model.addConstr(
        variables.sum(doctor, "*", "*") <= MAX_SHIFTS, f"{doctor}_max_shifts"
    )

for dep, doctors in dperartments_doctors.items():
    build_luck_worker_constraint(
        model, variables, max_work_vars, (dep, doctors), mode="unluckiest"
    )
    build_luck_worker_constraint(
        model, variables, min_work_vars, (dep, doctors), mode="luckiest"
    )


# model.addConstr(variables.sum("r_gine_1", "*", "*") <= 4, "r_gine_1_3_shifts")
# model.addConstr(variables.sum("r_gine_2", "*", "*") <= 4, "r_gine_2_3_shifts")

# model.addConstr(variables.sum("r_ost_1", "*", "*") <= 4, "r_ost_1_3_shifts")

# model.addConstr(variables.sum("r_ost_2", "*", "*") <= 4, "r_ost_2_3_shifts")

# model.addConstr(variables.sum("r_ost_3", "*", "*") <= 4, "r_ost_3_3_shifts")


# Set the objective in order to let in department shift to be equally distributed


model.setObjective(max_work_vars.sum("*") - min_work_vars.sum("*"), GRB.MINIMIZE)
model.optimize()

if model.status == GRB.OPTIMAL:
    for var in variables:
        to_print = f"{var[0]}"
        if variables[var].x:
            to_print += f" is working on {ID_TO_WEEKDAY_NAME[idx_dow[var[1]]]} | {year}-{month}-{var[1] + 1} | {SHIFT_NAMES[var[2]]}"
        else:
            to_print += f" is not working on {ID_TO_WEEKDAY_NAME[idx_dow[var[1]]]} | {year}-{month}-{var[1] + 1} | {SHIFT_NAMES[var[2]]}"

        print(to_print)
