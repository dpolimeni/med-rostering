from typing import Dict, List, Tuple
from gurobipy import Model, GRB, quicksum, tupledict
from departments_data import departments_constraint


def build_consecutive_shift_constraint(
    model: Model, assignments_vars: tupledict, doctor_names: List[str], month_days: int
) -> None:
    """Builds and Add the constraint to the model that no one can work two consecutive shifts

    Args:
        model (Model): Gurobi model
        assignments_vars (tupledict): like (doctor_name, day, shift) -> binary_var
    """
    # Iterate over doctors
    for doctor in doctor_names:
        for day in range(month_days):
            # No consecutive shifts
            model.addConstr(
                assignments_vars[doctor, day, 0] + assignments_vars[doctor, day, 1]
                <= 1,
                f"no_consecutive_{doctor}_{day}",
            )
            if day != month_days - 1:
                model.addConstr(
                    assignments_vars[doctor, day, 1]
                    + assignments_vars[doctor, day + 1, 0]
                    <= 1,
                    f"no_consecutive_{doctor}_{day}_night_{day + 1}_morning",
                )
                model.addConstr(
                    assignments_vars[doctor, day, 1]
                    + assignments_vars[doctor, day + 1, 0]
                    + assignments_vars[doctor, day + 1, 1]
                    <= 1,
                    f"no_consecutive_{doctor}_{day}_night_{day + 1}_",
                )

    return


def build_custom_constraint(
    model: Model, assignment_vars: tupledict, doctor_name: str, day: int, shift: int
) -> None:
    """Build a custom contraint of a doctor that is unavailable in specific day and shift

    Args:
        model (Model): Gurobi model
        assignment_vars (tupledict): like (doctor_name, day, shift) -> binary_var
        doctor_name (str): Unique Name of the doctor
        day (int): month day (0-31)
        shift (int): 0 for morning, 1 for night
    """
    model.addConstr(
        assignment_vars[doctor_name, day, shift] == 0,
        name=f"custom_constraint_{doctor_name}_{day}_{shift}",
    )
    return


def build_doctors_per_shift_constraint(
    model: Model,
    assignments_vars: tupledict,
    days: int,
    min_doctors_per_shift: int = 1,
    max_doctors_per_shift: int = 1,
) -> None:
    """Builds and Add the constraint to the model that there must be at least min_doctors_per_shift and at most max_doctors_per_shift

    Args:
        model (Model): Gurobi model
        assignments_vars (tupledict): like (doctor_name, day, shift) -> binary
        days (int): Number of days in the month
        min_doctors_per_shift (int): Minimum number of doctors per shift
        max_doctors_per_shift (int): Maximum number of doctors per shift
    """
    for shift in range(2):
        for day in range(days):
            model.addConstr(
                assignments_vars.sum("*", day, shift) >= min_doctors_per_shift,
                name=f"min_{min_doctors_per_shift}_per_shift_{day}_{shift}",
            )
            model.addConstr(
                assignments_vars.sum("*", day, shift) <= max_doctors_per_shift,
                name=f"max_{max_doctors_per_shift}_per_shift_{day}_{shift}",
            )
    return


# STRATEGY 1 all doctors must work at least floor(total-shifts/num_doctors) and at most (total-shifts/num_doctors) + 1
def build_shifts_range_contraints(
    model: Model,
    assignments_vars: tupledict,
    doctor_names: List[str],
    month_days: int,
    relaxation: int = 0,
) -> None:
    """Creates constraint in order to follow a simple CPSAT strategy:
    - Given K doctors
    - Given N shifts in the month
    - Each doctor must work at least floor(N/K) and at most (N/K) + 1 shifts + relaxation

    Args:
        model (Model): Gurobi model
        assignment_vars (tupledict): like (doctor_name, day, shift) -> binary_var
        doctor_names (List[str]): List of Unique Name of the doctors
        month_days (int): Number of days in the month
    """
    min_shifts = int(month_days / len(doctor_names))
    max_shifts = min_shifts + 1 + relaxation
    for doctor in doctor_names:
        model.addConstr(
            assignments_vars.sum(doctor, "*", "*") >= min_shifts,
            f"min_shifts_{doctor}_{min_shifts}",
        )
        model.addConstr(
            assignments_vars.sum(doctor, "*", "*") <= max_shifts,
            f"max_shifts_{doctor}_{max_shifts}",
        )
    return


def build_department_constraints(
    model: Model,
    assignments_vars: tupledict,
    department: str,
    doctor_name: str,
    # dayidx_to_dow: Dict[int, str],
    dow_to_dayidx: Dict[str, List[int]],
) -> None:
    """Generate the constraints for the doctor based on the department

    Args:
        model (Model): Gurobi model
        assignments_vars (tupledict): Ok
        department (str): name of the department
        doctor (str): Unique Name of the doctor
    """
    constraints = departments_constraint[department]
    for constraint in constraints:
        day, shift = constraint
        for dayidx in dow_to_dayidx[day]:
            build_custom_constraint(model, assignments_vars, doctor_name, dayidx, shift)
    return


def build_cross_department_constraint(
    model: Model,
    assignments_vars: tupledict,
    department_low_doctors: Tuple[str, List[str]],
    department_high_doctors: Tuple[str, List[str]],
):
    """Create a cross department constraint in order to set department_low doctors to work less than department_high doctors

    Args:
        model (Model): Gurobi model
        assignments_vars (tupledict): like (doctor_name, day, shift) -> binary_var
        department_low_doctors (str): the name of the doctors in the department that should work less
        department_high_doctors (str): the name of the doctors in the department that should work more
    """
    # Relaxed version of the constraint with sum of work done in department_low <= sum of work done in department_high (along all doctors)
    low_sum = sum(
        assignments_vars.sum(doctor, "*", "*") for doctor in department_low_doctors[1]
    )
    high_sum = sum(
        assignments_vars.sum(doctor, "*", "*") for doctor in department_high_doctors[1]
    )
    model.addConstr(
        low_sum
        <= high_sum * len(department_low_doctors[1]) / len(department_high_doctors[1])
        - len(department_low_doctors[1]) / len(department_high_doctors[1]),
        f"cross_department_constraint_{department_low_doctors[0]}_{department_high_doctors[0]}",
    )
    return


def build_luck_worker_constraint(
    model: Model,
    assignment_vars: tupledict,
    helping_vars: tupledict,
    department_doctors: Tuple[str, List[str]],
    mode: str = "luckiest", # luckiest or unluckiest
):
    """Build a constraint that forces the helping variables to be greater than the sum of the shifts of the doctors in the department that works the most

    Args:
        model (Model): Gurobi model
        assignment_vars (tupledict): assignment of the doctors to the shifts delta_mjk (doctor, day, shift) -> binary_var
        helping_vars (tupledict): helping variables for department v_j = sum(delta_mjk) (department, day, shift) of the most unlucky doctor -> continuous_var
        department_doctors (Tuple[str, List[str]]): department name and list of doctors in the department
    """
    department, doctors = department_doctors
    for doctor in doctors:
        if mode == "luckiest":
            model.addConstr(
                helping_vars[department] <= assignment_vars.sum(doctor, "*", "*"),
                name=f"luckiest_worker_{department}_{doctor}",
            )
        elif mode == "unluckiest":  
            model.addConstr(
                helping_vars[department] >= assignment_vars.sum(doctor, "*", "*"),
                name=f"unlucky_worker_{department}_{doctor}",
            )

    return


if __name__ == "__main__":
    model = Model("Shifts-Manager")
    vars = model.addVars(
        ["alessia", "marco"], list(range(31)), [0, 1], vtype=GRB.BINARY, name="x"
    )
    # Al vars less than 1
    # for idx, var in enumerate(vars):
    #     model.addConstr(vars[var] <= 1, f"{idx}")
    # model.addConstr(vars.sum("*", "*", 0) <= 0)
    build_consecutive_shift_constraint(model, vars, ["alessia", "marco"], 31)
    model.setObjective(vars.sum("*", "*", "*"), GRB.MAXIMIZE)
    print(model.getVars())

    model.optimize()
    for var in vars:
        print(var, vars[var].x)
