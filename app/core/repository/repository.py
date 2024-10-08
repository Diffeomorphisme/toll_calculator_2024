import abc
from datetime import time, datetime

from app.vehicle.model import VehiclePassage, VehicleActivity

"""Both TOLL_FEE_BREAKDOWN and TOLL_FEE_FREE_VEHICLES should be stored in a
database or another place that can be reached by the code but NOT directly in
the code. For the sake of this exercise, though, they will be stored in the
repository file."""

TOLL_FEE_BREAKDOWN = [
    {
        "id": 0,
        "start_time": time(6, 0),
        "end_time": time(6, 30),
        "fee": 8
    },
    {
        "id": 1,
        "start_time": time(6, 30),
        "end_time": time(7, 0),
        "fee": 13
    },
    {
        "id": 2,
        "start_time": time(7, 0),
        "end_time": time(8, 0),
        "fee": 18
    },
    {
        "id": 3,
        "start_time": time(8, 0),
        "end_time": time(8, 30),
        "fee": 13
    },
    {
        "id": 4,
        "start_time": time(8, 30),
        "end_time": time(15, 0),
        "fee": 8
    },
    {
        "id": 5,
        "start_time": time(15, 0),
        "end_time": time(15, 30),
        "fee": 13
    },
    {
        "id": 6,
        "start_time": time(15, 30),
        "end_time": time(17, 0),
        "fee": 18
    },
    {
        "id": 7,
        "start_time": time(17, 0),
        "end_time": time(18, 0),
        "fee": 13
    },
    {
        "id": 8,
        "start_time": time(18, 0),
        "end_time": time(18, 30),
        "fee": 8
    },
    {
        "id": 9,
        "start_time": time(18, 30),
        "end_time": time(6, 0),
        "fee": 0
    },
]


TOLL_FEE_FREE_VEHICLES = {
    "Motorbike",
    "Tractor",
    "Emergency",
    "Diplomat",
    "Foreign",
    "Military"
}


class AbstractVehicleRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, vehicle_number: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, vehicle_passage_data: VehiclePassage):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, vehicle_number: str):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, vehicle_passage_data: VehiclePassage):
        raise NotImplementedError


class AbstractRepositoryTollFee(abc.ABC):
    @abc.abstractmethod
    def get(self, time_of_day: datetime):
        raise NotImplementedError


class AbstractRepositoryNoFeeVehicles(abc.ABC):
    @abc.abstractmethod
    def get(self, target_vehicle_type: str):
        raise NotImplementedError


class FakeVehicleRepository(AbstractVehicleRepository):
    def __init__(self, vehicles: list[VehicleActivity]):
        self._vehicles = vehicles

    def get(self, vehicle_number: str) -> VehicleActivity | None:
        for vehicle in self._vehicles:
            if vehicle.vehicle_number == vehicle_number:
                return vehicle
        return None

    def get_all(self) -> list[VehicleActivity]:
        return self._vehicles

    def add(self, vehicle_passage_data: VehiclePassage) -> None:
        self._vehicles.append(
            VehicleActivity(
                vehicle_number=vehicle_passage_data.vehicle_number,
                vehicle_type=vehicle_passage_data.vehicle_type,
                vehicle_activity=[vehicle_passage_data.date_time]
            )
        )

    def update(self, vehicle_passage_data: VehiclePassage) -> None:
        for vehicle in self._vehicles:
            if vehicle.vehicle_number == vehicle_passage_data.vehicle_number:
                vehicle.vehicle_activity.append(vehicle_passage_data.date_time)
                vehicle.vehicle_activity.sort()
                return

    def delete(self, vehicle_number: str) -> None:
        for vehicle in self._vehicles:
            if vehicle.vehicle_number == vehicle_number:
                self._vehicles.remove(vehicle)
                return


class FakeTollFeeRepository(AbstractRepositoryTollFee):
    def __init__(self, toll_fee_breakdown: list[dict]):
        self._toll_fee_breakdown = toll_fee_breakdown

    def get(self, target_datetime: datetime) -> int:
        for toll_fee in self._toll_fee_breakdown:
            start_time: time = toll_fee.get("start_time")
            end_time: time = toll_fee.get("end_time")
            time_of_day = time(target_datetime.hour, target_datetime.minute)
            if start_time <= end_time:
                if start_time <= time_of_day < end_time:
                    return toll_fee.get("fee")
            else:
                if start_time <= time_of_day or time_of_day <= end_time:
                    return toll_fee.get("fee")


class FakeNoFeeVehicleRepository(AbstractRepositoryNoFeeVehicles):
    def __init__(self, toll_fee_free_vehicles: set[str]):
        self._toll_fee_free_vehicles = toll_fee_free_vehicles

    def get(self, target_vehicle_type: str) -> bool:
        for vehicle in self._toll_fee_free_vehicles:
            if vehicle.lower() == target_vehicle_type.lower():
                return True
        return False


vehicle_repository = FakeVehicleRepository([])
toll_fee_repository = FakeTollFeeRepository(TOLL_FEE_BREAKDOWN)
toll_fee_free_vehicles_repository = FakeNoFeeVehicleRepository(
    TOLL_FEE_FREE_VEHICLES
)
