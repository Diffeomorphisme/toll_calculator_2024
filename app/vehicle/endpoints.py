from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends
)

from app import logger
from app.vehicle.model import VehiclePassage


router = APIRouter(
    prefix="/vehicle", tags=["vehicle"]
)


@router.post("")
async def register_vehicle_passage(
        vehicle_passage_data: VehiclePassage,
        background_tasks: BackgroundTasks,
        # db: SessionLocal = Depends(get_db)
) -> str:
    return f"""Nice car {vehicle_passage_data.vehicle_number} of type {vehicle_passage_data.vehicle_type}
    Spotted at {vehicle_passage_data.date_time}"""
