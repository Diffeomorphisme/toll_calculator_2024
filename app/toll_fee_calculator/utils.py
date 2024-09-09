import holidays
from datetime import date, datetime


def check_if_date_is_holiday(target_date: date) -> bool:
    se_holidays = holidays.country_holidays("SE")
    return target_date in se_holidays


def check_if_date_is_weekend(target_date: date) -> bool:
    return target_date.weekday() >= 5


def check_if_date_is_target_date(
        input_date: datetime, target_date: date
) -> bool:
    return input_date.date() == target_date
