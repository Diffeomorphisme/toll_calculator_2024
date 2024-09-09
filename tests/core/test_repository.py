from unittest import TestCase
from datetime import datetime

from app.core.repository.repository import (
    vehicle_repository,
    toll_fee_repository,
    toll_fee_free_vehicles_repository
)
from app.vehicle.model import VehiclePassage


class TestTollFeeRepository(TestCase):
    def test_toll_fee_length(self):
        self.assertEqual(len(toll_fee_repository._toll_fee_breakdown), 10)

    def test_no_fee_morning(self):
        target_time = datetime(1, 1, 1, 5, 0)
        target_fee = 0
        self.assertEqual(toll_fee_repository.get(target_time), target_fee)

    def test_no_fee_evening(self):
        target_time = datetime(1, 1, 1, 23, 0)
        target_fee = 0
        self.assertEqual(toll_fee_repository.get(target_time), target_fee)

    def test_specific_fee(self):
        target_time = datetime(1, 1, 1, 7, 25)
        target_fee = 18
        self.assertEqual(toll_fee_repository.get(target_time), target_fee)


class TestVehicleRepository(TestCase):
    def test_adding_vehicle(self):
        vehicle_number = "1234567"
        vehicle_type = "Car"
        time_of_passage = datetime.now()

        vehicle_to_add = VehiclePassage(
                vehicle_number=vehicle_number,
                vehicle_type=vehicle_type,
                date_time=time_of_passage
        )

        self.assertIsNone(vehicle_repository.get(vehicle_number))
        vehicle_repository.add(vehicle_to_add)
        self.assertEqual(
            vehicle_repository.get(vehicle_number).vehicle_number,
            vehicle_number
        )
        self.assertEqual(len(vehicle_repository.get_all()), 1)

    # Other tests should be written for all crud operations


class TestTollFeeFreeVehiclesRepository(TestCase):
    def test_toll_fee_free_vehicle(self):
        vehicle_type = "diplomat"
        self.assertTrue(toll_fee_free_vehicles_repository.get(vehicle_type))

    def test_non_toll_fee_free_vehicle(self):
        vehicle_type = "car"
        self.assertFalse(toll_fee_free_vehicles_repository.get(vehicle_type))
