from dao import anomaly_dao, trace_dao
from domain.models import TraceModel, AnomalyTrace


# This service is made primarily for accessing historical data to show to the viewer

#
# should register and store in some storage (file on a disk, sqlite database - your
# choice) the history of walking for at least 10 minutes backward to current
# time to allow review of historical values;

# RUN ONLY ONCE ON STARTUP

def get_traces(patient_id: int) -> [TraceModel]:
    return trace_dao.get_traces(patient_id)


def get_anomalies_for_patient(patient_id: int) -> [AnomalyTrace]:
    return anomaly_dao.get_anomaly_traces(patient_id)


def get_anomaly_for_patient(patient_id: int, anomaly_start: str, anomaly_end: str) -> AnomalyTrace:
    return anomaly_dao.get_anomaly_trace(patient_id=patient_id, anomaly_start=anomaly_start, anomaly_end=anomaly_end)
