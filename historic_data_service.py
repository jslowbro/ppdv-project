import anomaly_dao
import dao
from models import TraceModel, AnomalyTrace
import threading
import time
import tesla_client
import datetime

# This service is made primarily for accessing historical data to show to the viewer

#
# should register and store in some storage (file on a disk, sqlite database - your
# choice) the history of walking for at least 10 minutes backward to current
# time to allow review of historical values;

# RUN ONLY ONCE ON STARTUP

anomaly_alarm_cache = dict()


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


def get_anomalies_for_patient(patient_id: int) -> [AnomalyTrace]:
    return anomaly_dao.get_anomaly_traces(patient_id)


def get_anomaly_for_patient(patient_id: int, anomaly_start: str, anomaly_end: str) -> AnomalyTrace:
    return anomaly_dao.get_anomaly_trace(patient_id=patient_id, anomaly_start=anomaly_start, anomaly_end=anomaly_end)


def fetch_and_save_trace(patient_id: int):
    trace = tesla_client.get_patient_trace(patient_id)
    # If anomaly already registered for patient
    if patient_id in anomaly_alarm_cache:
        if is_anomaly_detected(trace):
            print('ANOMALY DETECTED - SAVING TO CACHE, PATIENT ID = {}'.format(patient_id))
            # Anomaly continuing, append it to traceList
            anomaly_alarm_cache[patient_id].traces.append(trace.__dict__)
        else:
            # Anomaly stopped, update end time, save trace to db, clear cache
            print('ANOMALY STOPPED - SAVING TO DB, PATIENT ID = {}'.format(patient_id))
            anomaly_trace = anomaly_alarm_cache[patient_id]
            anomaly_trace.anomaly_end = str(datetime.datetime.now())
            anomaly_dao.save_anomaly_trace(anomaly_alarm_cache[patient_id])
            del anomaly_alarm_cache[patient_id]
    # Anomaly not registered for patient
    else:
        if is_anomaly_detected(trace):
            print('ANOMALY DETECTED - CACHING AN ANOMALY, PATIENT ID = {}'.format(patient_id))
            # Register anomaly in cache
            anomaly_alarm_cache[patient_id] = AnomalyTrace(patient_id, str(datetime.datetime.now()), "",
                                                           [trace.__dict__])
        else:
            # no anomaly detected save normal trace
            dao.save_trace(trace)


def is_anomaly_detected(trace_model: TraceModel):
    if trace_model.l0a | trace_model.l1a | trace_model.l2a | trace_model.r0a | trace_model.r1a | trace_model.r2a:
        return True
    return False
