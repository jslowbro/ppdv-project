import json

from models import Reading, Trace, Sensor, TraceModel, AnomalyTrace


# This file handles creating objects (Reading, Trace, Sensor) from Python data structures (dictionaries) and json represenations

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


def trace_model_from_json(reading_json, patient_id) -> TraceModel:
    reading_dict = json.loads(reading_json)
    return trace_model_from_reading_dict(reading_dict, patient_id)


def trace_model_from_reading_dict(reading_dict, patient_id) -> TraceModel:
    trace_dict = reading_dict['trace']
    sensors_list = trace_dict['sensors']
    tm = TraceModel(
        trace_id=trace_dict['id'],
        patient_id=patient_id,
        l0=sensors_list[0]['value'],
        l0a=sensors_list[0]['anomaly'],
        l1=sensors_list[1]['value'],
        l1a=sensors_list[1]['anomaly'],
        l2=sensors_list[2]['value'],
        l2a=sensors_list[2]['anomaly'],
        r0=sensors_list[3]['value'],
        r0a=sensors_list[3]['anomaly'],
        r1=sensors_list[4]['value'],
        r1a=sensors_list[4]['anomaly'],
        r2=sensors_list[5]['value'],
        r2a=sensors_list[5]['anomaly']
    )
    return tm


def trace_model_from_dict(trace_dict):
    tm = TraceModel(
        trace_id=trace_dict['trace_id'],
        patient_id=trace_dict['patient_id'],
        l0=trace_dict['l0'],
        l0a=trace_dict['l0a'],
        l1=trace_dict['l1'],
        l1a=trace_dict['l1a'],
        l2=trace_dict['l2'],
        l2a=trace_dict['l2a'],
        r0=trace_dict['r0'],
        r0a=trace_dict['r0a'],
        r1=trace_dict['r1'],
        r1a=trace_dict['r1a'],
        r2=trace_dict['r2'],
        r2a=trace_dict['r2a']
    )
    return tm


def anomaly_trace_from_dict(anomaly_trace):
    at = AnomalyTrace(
        patient_id=anomaly_trace['patient_id'],
        anomaly_start=anomaly_trace['anomaly_start'],
        anomaly_end=anomaly_trace['anomaly_end'],
        traces=[t for t in anomaly_trace['traces']]
    )
    return at
