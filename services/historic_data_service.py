from dao import anomaly_dao, trace_dao
from domain.models import TraceModel, AnomalyTrace, Reading
from services import tesla_service


def get_traces(patient_id: int) -> [TraceModel]:
    return trace_dao.get_traces(patient_id)


def get_anomalies_for_patient(patient_id: int) -> [AnomalyTrace]:
    return anomaly_dao.get_anomaly_traces(patient_id)


def get_anomaly_for_patient(patient_id: int, anomaly_start: str, anomaly_end: str) -> AnomalyTrace:
    return anomaly_dao.get_anomaly_trace(patient_id=patient_id, anomaly_start=anomaly_start, anomaly_end=anomaly_end)


def get_reading(patient_id: int) -> [Reading]:
    return tesla_service.get_patient_reading(patient_id)
