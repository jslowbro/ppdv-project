import json

from models import Reading, Trace, Sensor

#This file handles creating objects (Reading, Trace, Sensor) from Python data structures (dictionaries) and json represenations

def unmarshal_reading(reading_dict):
    r = Reading(
        reading_dict['birthdate'],
        reading_dict['disabled'],
        reading_dict['firstname'],
        reading_dict['id'],
        reading_dict['lastname'],
        unmarshal_trace(reading_dict['trace'])
    )
    return r


def unmarshal_trace(trace_dict):
    t = Trace(
        trace_dict['id'],
        trace_dict['name'],
        sensors=[unmarshal_sensor(s) for s in trace_dict['sensors']]
    )
    return t


def unmarshal_sensor(sensors_dict):
    s = Sensor(
        sensors_dict['anomaly'],
        sensors_dict['id'],
        sensors_dict['name'],
        sensors_dict['value']
    )
    return s


def reading_from_json(reading_json):
    return unmarshal_reading(json.loads(reading_json))
