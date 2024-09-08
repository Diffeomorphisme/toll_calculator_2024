from app import logger
from app.vehicle.model import VehiclePassage
from app.core.repository.repository import vehicle_repository


def process_vehicle_toll_information(vehicle_passage_data: VehiclePassage):
    existing_vehicle = vehicle_repository.get(
        vehicle_passage_data.vehicle_number
    )
    if existing_vehicle:
        logger.info("Existing vehicle, updating activity")
        vehicle_repository.update(vehicle_passage_data)
    else:
        logger.info("New vehicle, creating record")
        vehicle_repository.add(vehicle_passage_data)
