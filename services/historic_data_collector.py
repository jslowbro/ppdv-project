import datetime
import threading
import time

from dao import anomaly_dao, trace_dao
from client import tesla_client
from services import utils
from domain.models import AnomalyTrace

anomaly_alarm_cache = dict()


# RUN ONLY ONCE ON STARTUP
def start_collecting_historic_data():
    t1 = threading.Thread(target=import_data_from_tesla)
    t1.start()


def import_data_from_tesla():
    while True:
        time.sleep(1)
        for i in range(1, 7):
            fetch_and_save_trace(i)


def fetch_and_save_trace(patient_id: int):
    trace = tesla_client.get_patient_trace(patient_id)
    # If anomaly already registered for patient
    if patient_id in anomaly_alarm_cache:
        if utils.is_anomaly_detected(trace):
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
        if utils.is_anomaly_detected(trace):
            print('ANOMALY DETECTED - CACHING AN ANOMALY, PATIENT ID = {}'.format(patient_id))
            # Register anomaly in cache
            anomaly_alarm_cache[patient_id] = AnomalyTrace(patient_id, str(datetime.datetime.now()), "",
                                                           [trace.__dict__])
        else:
            # no anomaly detected save normal trace
            trace_dao.save_trace(trace)
