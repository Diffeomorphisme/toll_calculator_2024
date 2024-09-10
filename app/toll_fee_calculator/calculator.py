import datetime as _datetime
from datetime import date, datetime

from app.core.repository.repository import (
    vehicle_repository,
    toll_fee_repository,
    toll_fee_free_vehicles_repository
)
from app.vehicle.model import VehicleActivity, VehicleWithFee
from app.toll_fee_calculator.utils import (
    check_if_date_is_holiday,
    check_if_date_is_weekend,
    check_if_date_is_target_date
)
from app.toll_fee_calculator.export import send_toll_fees_to_payment_api


# This is stored in the code but
MAX_FEE = 60


def run_toll_fee_calculations() -> None:
    """Gather the toll fees and send them to the API dealing with payments"""
    vehicles_with_fees = calculate_toll_fee_for_all_vehicles()
    send_toll_fees_to_payment_api(vehicles_with_fees)


def calculate_toll_fee_for_all_vehicles() -> list[VehicleWithFee]:
    target_date = date.today()
    vehicles_with_fees: list[VehicleWithFee] = []
    for vehicle in vehicle_repository.get_all():
        vehicle_fee = calculate_toll_fee_for_single_vehicle(
            vehicle, target_date
        )
        vehicles_with_fees.append(
            VehicleWithFee(
                vehicle_number=vehicle.vehicle_number,
                toll_fee=vehicle_fee
            )
        )
    return vehicles_with_fees


def calculate_toll_fee_for_single_vehicle(
        vehicle: VehicleActivity, target_date: date
) -> int:
    """Run the toll fee calculations for a single vehicle at a given date."""

    if check_if_date_is_holiday(target_date):   # No fee during holidays
        return 0
    if check_if_date_is_weekend(target_date):   # No fee during weekends
        return 0

    vehicle_is_toll_fee_free = toll_fee_free_vehicles_repository.get(
        vehicle.vehicle_type
    )
    if vehicle_is_toll_fee_free:    # No fee for certain vehicles
        return 0

    target_vehicle_activity = list(
        filter(
            lambda x: check_if_date_is_target_date(x, target_date),
            vehicle.vehicle_activity
        )
    )

    # The actual calculations of the toll fee for the vehicle on the target day
    total_fee = 0
    temp_fee = toll_fee_repository.get(target_vehicle_activity[0])
    start_time: datetime = target_vehicle_activity[0]
    for index, toll_passage in enumerate(target_vehicle_activity):
        if toll_passage < start_time + _datetime.timedelta(hours=1):
            # only the biggest fee applies within an hour interval
            temp_fee = max(
                temp_fee,
                toll_fee_repository.get(toll_passage)
            )
        else:
            total_fee += temp_fee
            temp_fee = toll_fee_repository.get(toll_passage)
            start_time = toll_passage
            if total_fee >= MAX_FEE:
                return MAX_FEE
        if index == len(target_vehicle_activity) - 1:
            total_fee += temp_fee
            if total_fee >= MAX_FEE:
                return MAX_FEE

    return total_fee
