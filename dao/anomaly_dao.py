from tinydb import TinyDB, Query

from domain.models import AnomalyTrace
from domain import models_marshaller

# This file handles connecting to the database (writing and reading to file historic-readings.json)
# It breaks all the time so we'll be probably using a different database in the future

db = TinyDB('db/anomaly-readings.json', ensure_ascii=False)


def save_anomaly_trace(trace: AnomalyTrace):
    return db.table(str(trace.patient_id)).insert(trace.__dict__)


def get_anomaly_traces(patient_id: int) -> [AnomalyTrace]:
    q = Query()
    ret = db.table(str(patient_id)).search((q.patient_id == patient_id))
    return [models_marshaller.anomaly_trace_from_dict(d) for d in ret]


def get_anomaly_trace(patient_id: int, anomaly_start: str, anomaly_end: str) -> AnomalyTrace:
    q = Query()
    ret = db.table(str(patient_id)).search(
        (q.patient_id == patient_id) & (q.anomaly_start == anomaly_start) & (anomaly_end == anomaly_end))
    return [models_marshaller.anomaly_trace_from_dict(d) for d in ret][0]
