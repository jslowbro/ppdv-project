import dao
import tesla_service
from models import Reading, TraceModel
import threading
import time
import tesla_client


# This service is made primarily for accessing historical data to show to the viewer

#
# should register and store in some storage (file on a disk, sqlite database - your
# choice) the history of walking for at least 10 minutes backward to current
# time to allow review of historical values;

# RUN ONLY ONCE ON STARTUP
def start_collecting_historic_data():
    t1 = threading.Thread(target=import_data_from_tesla)
    t1.start()


def import_data_from_tesla():
    while True:
        time.sleep(1)
        for i in range(1, 7):
            fetch_and_save_trace(i)


def get_traces(patient_id: int) -> [TraceModel]:
    return dao.get_traces(patient_id)


def get_sensor(reading_list, sensor: str):
    sensor_list = map(lambda r: get_sensor_from_reading(r, sensor), reading_list)
    return sensor_list


def get_sensor_from_reading(reading: Reading, sensor_name: str):
    iter = filter(lambda s: s.name == sensor_name, reading.trace.sensors)
    return list(iter)[0]


def fetch_and_save_trace(patient_id: int):
    trace = tesla_client.get_patient_trace(patient_id)
    dao.save_trace(trace)
