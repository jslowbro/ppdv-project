from tinydb import TinyDB, Query

from domain.models import TraceModel
from domain import models_marshaller

# This file handles connecting to the database (writing and reading to file historic-readings.json)
# It breaks all the time so we'll be probably using a different database in the future

db = TinyDB('db/historic-readings.json', ensure_ascii=False)


# save TraceModel to database
def save_trace(trace: TraceModel):
    return db.table(str(trace.patient_id)).insert(trace.__dict__)


# read Traces by Trace Id
def get_traces(patient_id: int) -> [TraceModel]:
    q = Query()
    ret = db.table(str(patient_id)).search((q.patient_id == patient_id))
    return [models_marshaller.trace_model_from_dict(d) for d in ret]
