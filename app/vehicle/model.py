from pydantic import BaseModel
from datetime import datetime


class Vehicle(BaseModel):
    vehicle_number: str


class VehicleWithType(Vehicle):
    vehicle_type: str


class VehiclePassage(VehicleWithType):
    date_time: datetime


class VehicleActivity(VehicleWithType):
    vehicle_activity: list[datetime]


class VehicleWithFee(Vehicle):
    toll_fee: int
