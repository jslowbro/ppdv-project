import dao
from models import Reading

#This service is made primarily for accessing historical data to show to the viewer

#
# should register and store in some storage (file on a disk, sqlite database - your
# choice) the history of walking for at least 10 minutes backward to current
# time to allow review of historical values;

def get_readings(first_name: str, last_name: str):
    return dao.get_readings(first_name, last_name)


def get_sorted_readings(first_name: str, last_name: str):
    return sorted(get_readings(first_name, last_name), key=lambda x: x.trace.id, reverse=True)


def get_sensor(first_name: str, last_name: str, sensor: str):
    return get_sensor(get_readings(first_name, last_name), sensor)


def get_sensor(reading_list, sensor: str):
    sensor_list = map(lambda r: get_sensor_from_reading(r, sensor), reading_list)
    return sensor_list


def get_sensor_from_reading(reading: Reading, sensor_name: str):
    iter = filter(lambda s: s.name == sensor_name, reading.trace.sensors)
    return list(iter)[0]
