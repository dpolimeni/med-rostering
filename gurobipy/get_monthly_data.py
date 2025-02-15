from datetime import datetime
from collections import defaultdict
import calendar


# Given a month obtain a dict with {idx: day_of_week} and {day_of_week: [idx0, idx1, ...]}
def get_monthly_data(date: str):
    """Given a date extract the month and return a dict with {idx: day_of_week}

    Args:
        date (str): Date in the format 'YYYY-MM-DD'

    Returns:
        idx_to_day_of_week (dict): idx -> day_of_week
        day_of_week_to_idx (dict): day_of_week -> idx0, idx1, ...
    """
    datetime_data = datetime.strptime(date, "%Y-%m-%d")
    # Extract
    num_days = calendar.monthrange(datetime_data.year, datetime_data.month)[1]
    day_dow_output = {}
    dow_days_output = defaultdict(list)
    for day in range(1, num_days + 1):
        dow = datetime_data.replace(day=day).weekday()
        # day_of_week = calendar.day_name[datetime_data.replace(day=day).weekday()]
        day_dow_output[day - 1] = dow
        dow_days_output[dow].append(day - 1)
    return day_dow_output, dow_days_output


if __name__ == "__main__":
    date = input("Enter the date: ")
    print(get_monthly_data(date))
