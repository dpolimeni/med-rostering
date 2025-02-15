# List of departments and their constraints for each department by day and turn
SHIFT_NAMES = ["morning", "night"]
ID_TO_WEEKDAY_NAME = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}
# List of departments and their constraints as a list of tuples (day, shift)
departments_constraint = {
    # No Monday morning, tuesday morning & nigth, Friday night, Saturday morning & night, Sunday morning
    "reparto_ostetricia": [(0, 1), (1, 0), (1, 1), (4, 1), (5, 0), (5, 1), (6, 0)],
    # No constraint
    "ambulatorio_ostetricia": [],
    # No Monday night, Tuesday morning & night, Wednesday night, Thursday morning & night
    "day_hospital_ostetricia": [(0, 1), (1, 0), (1, 1), (2, 1), (3, 0), (3, 1)],
    # No Monday morning & night, Tuesday morning & night, Friday night, Saturday morning & night, Sunday morning & night
    "reparto_ginecologia": [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
        (4, 1),
        (5, 0),
        (5, 1),
        (6, 0),
    ],
    # No constraint
    "ambulatorio_ginecologia": [],
    #
    "sala_operatoria": [],
}
