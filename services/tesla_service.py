from client import tesla_client


# This one handles using the tesla client
from domain.models import Reading


def get_patient_reading(reading_id: id) -> Reading:
    reading = tesla_client.get_patient_reading(reading_id)
    return reading
