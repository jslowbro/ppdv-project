import dao
import tesla_client


# This one handles using the tesla client

def get_patient_reading(reading_id: id):
    reading = tesla_client.get_patient_reading(reading_id)
    return reading
