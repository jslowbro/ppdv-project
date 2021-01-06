import dao
import tesla_client


# This one handles using the tesla client

def get_patient_reading(reading_id: id):
    reading = tesla_client.get_patient_reading(reading_id)
    return reading


def get_and_save_patient_reading(reading_id: id):
    reading = tesla_client.get_patient_reading(reading_id)
    dao.insert_reading(reading)
    return reading
