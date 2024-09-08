from fastapi import (
    APIRouter,
    BackgroundTasks,
)

from app.vehicle.model import VehiclePassage
from app.vehicle.process import process_vehicle_toll_information


router = APIRouter(
    prefix="/vehicle", tags=["vehicle"]
)


@router.post("")
async def register_vehicle_passage(
        vehicle_passage_data: VehiclePassage,
        background_tasks: BackgroundTasks,
) -> None:
    background_tasks.add_task(process_vehicle_toll_information, vehicle_passage_data)
