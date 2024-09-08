from datetime import datetime, date

from app.core.repository.repository import vehicle_repository
from app.vehicle.model import VehicleActivity


def run_toll_fee_calculations() -> None:
    target_date = date.today()
    for vehicle in vehicle_repository.get_all():
        toll_fee = calculate_toll_fee_for_single_vehicle(vehicle, target_date)
    return


def calculate_toll_fee_for_single_vehicle(vehicle: VehicleActivity, target_date: date) -> int:
    pass
