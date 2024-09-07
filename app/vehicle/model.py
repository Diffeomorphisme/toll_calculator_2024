from pydantic import BaseModel
from datetime import datetime


class VehiclePassage(BaseModel):
    vehicle_number: str
    date_time: datetime
    vehicle_type: str
