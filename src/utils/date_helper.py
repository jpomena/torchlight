import numpy as np
import holidays
from datetime import date, timedelta


def get_business_days(start_date: date, end_date: date) -> int:
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        return 0

    if start_date > end_date:
        return 0

    start_year = start_date.year
    end_year = end_date.year
    years_to_check = list(range(start_year, end_year + 1))

    br_holidays = holidays.Brazil(years=years_to_check)

    original_holidays = list(br_holidays.keys())

    for holiday_date in original_holidays:
        weekday = holiday_date.weekday()

        if weekday == 1:
            bridge_day = holiday_date - timedelta(days=1)
            br_holidays[bridge_day] = "Bridge Day (to Tuesday holiday)"

        elif weekday == 3:
            bridge_day = holiday_date + timedelta(days=1)
            br_holidays[bridge_day] = "Bridge Day (from Thursday holiday)"

    holiday_list = [h.strftime('%Y-%m-%d') for h in br_holidays.keys()]

    business_days = np.busday_count(
        start_date.strftime('%Y-%m-%d'),
        (end_date + timedelta(days=1)).strftime('%Y-%m-%d'),
        holidays=holiday_list
    )

    return max(1, business_days)
