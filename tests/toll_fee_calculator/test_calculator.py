from unittest import TestCase
from datetime import datetime, date

from app.toll_fee_calculator.calculator import (
    calculate_toll_fee_for_single_vehicle
)
from app.vehicle.model import VehicleActivity


class TestTollFeeCalculator(TestCase):
    def test_holidays_fee_output(self):
        target_holiday = date(2024, 12, 24)
        recorded_activity = datetime(2024, 12, 24, 7, 0, 0)
        vehicle_activity = VehicleActivity(
            vehicle_number="123456",
            vehicle_type="car",
            vehicle_activity=[recorded_activity]
        )
        expected_fee = 0
        self.assertEqual(
            calculate_toll_fee_for_single_vehicle(
                vehicle_activity,
                target_holiday
            ),
            expected_fee
        )

    def test_weekends_fee_output(self):
        target_weekend_day = date(2024, 9, 8)
        recorded_activity = datetime(2024, 12, 24, 7, 0, 0)
        vehicle_activity = VehicleActivity(
            vehicle_number="123456",
            vehicle_type="car",
            vehicle_activity=[recorded_activity]
        )
        expected_fee = 0
        self.assertEqual(
            calculate_toll_fee_for_single_vehicle(
                vehicle_activity,
                target_weekend_day
            ),
            expected_fee
        )

    def test_toll_fee_free_vehicle(self):
        target_day = date(2024, 9, 9)
        recorded_activity = datetime(2024, 9, 9, 7, 0, 0)
        vehicle_type = "Emergency"
        vehicle_activity = VehicleActivity(
            vehicle_number="123456",
            vehicle_type=vehicle_type,
            vehicle_activity=[recorded_activity]
        )
        expected_fee = 0
        self.assertEqual(
            calculate_toll_fee_for_single_vehicle(
                vehicle_activity,
                target_day
            ),
            expected_fee
        )

    def test_single_fee(self):
        target_week_day = date(2024, 9, 9)
        recorded_activity = datetime(2024, 9, 9, 6, 30, 0)
        vehicle_activity = VehicleActivity(
            vehicle_number="123456",
            vehicle_type="car",
            vehicle_activity=[recorded_activity]
        )
        expected_fee = 13
        self.assertEqual(
            calculate_toll_fee_for_single_vehicle(
                vehicle_activity,
                target_week_day
            ),
            expected_fee
        )

    def test_multiple_fees_within_one_hour(self):
        target_week_day = date(2024, 9, 9)
        first_recorded_activity = datetime(2024, 9, 9, 6, 30, 0)
        second_recorded_activity = datetime(2024, 9, 9, 7, 29, 0)
        vehicle_activity = VehicleActivity(
            vehicle_number="123456",
            vehicle_type="car",
            vehicle_activity=[
                first_recorded_activity, second_recorded_activity
            ]
        )
        expected_fee = 18
        self.assertEqual(
            calculate_toll_fee_for_single_vehicle(
                vehicle_activity,
                target_week_day
            ),
            expected_fee
        )

    def test_maximum_fee_for_one_day(self):
        target_week_day = date(2024, 9, 9)
        recorded_activity = [
            datetime(2024, 9, 9, 6, 0, 0),
            datetime(2024, 9, 9, 7, 0, 0),
            datetime(2024, 9, 9, 8, 0, 0),
            datetime(2024, 9, 9, 9, 0, 0),
            datetime(2024, 9, 9, 10, 0, 0),
            datetime(2024, 9, 9, 11, 0, 0),
            datetime(2024, 9, 9, 12, 0, 0),
            datetime(2024, 9, 9, 13, 0, 0),
            datetime(2024, 9, 9, 14, 0, 0),
            datetime(2024, 9, 9, 15, 0, 0),
            datetime(2024, 9, 9, 16, 0, 0),
            datetime(2024, 9, 9, 17, 0, 0)
        ]
        vehicle_activity = VehicleActivity(
            vehicle_number="123456",
            vehicle_type="car",
            vehicle_activity=recorded_activity
        )
        expected_fee = 60
        self.assertEqual(
            calculate_toll_fee_for_single_vehicle(
                vehicle_activity,
                target_week_day
            ),
            expected_fee
        )

    def test_multiple_fees_over_several_slots(self):
        target_week_day = date(2024, 9, 9)
        recorded_activity = [
            datetime(2024, 9, 9, 6, 30, 0),
            datetime(2024, 9, 9, 7, 29, 0),
            datetime(2024, 9, 9, 14, 15, 0),
            datetime(2024, 9, 9, 15, 14, 0)
        ]
        vehicle_activity = VehicleActivity(
            vehicle_number="123456",
            vehicle_type="car",
            vehicle_activity=recorded_activity
        )
        expected_fee = 31
        self.assertEqual(
            calculate_toll_fee_for_single_vehicle(
                vehicle_activity,
                target_week_day
            ),
            expected_fee
        )
