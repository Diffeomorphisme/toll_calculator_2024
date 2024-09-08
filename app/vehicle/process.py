from app.vehicle.model import VehiclePassage
from app.core.repository.repository import vehicle_repository


def process_vehicle_toll_information(vehicle_passage_data: VehiclePassage):
    existing_vehicle = vehicle_repository.get(
        vehicle_passage_data.vehicle_number
    )
    if existing_vehicle:
        vehicle_repository.update(vehicle_passage_data)
    else:
        vehicle_repository.add(vehicle_passage_data)
