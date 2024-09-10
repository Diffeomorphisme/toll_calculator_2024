from app.vehicle.model import VehicleWithFee


def send_toll_fees_to_payment_api(
        vehicle_with_toll_fees: list[VehicleWithFee]
) -> None:
    """Send the toll fees to the payment API.
    This would export the toll fee calculations results to the right place
    in the right format. As of now it pretends to do something!
    """
    pass
