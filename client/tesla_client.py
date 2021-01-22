import requests

from domain.models import Reading, TraceModel
from domain import models_marshaller

# This file is used for accessing the API that we're meant to work with
url = "http://tesla.iem.pw.edu.pl:9080/v2/monitor/"


# Call tesla api and marshall the message into reading
def get_patient_reading(reading_id: int) -> Reading:
    response = requests.get(url + str(reading_id))
    reading = models_marshaller.unmarshal_reading(response.json())
    return reading


# Call tesla api and marshall the message into TraceModel
def get_patient_trace(patient_id: int) -> TraceModel:
    response = requests.get(url + str(patient_id))
    trace_model = models_marshaller.trace_model_from_reading_dict((response.json()), patient_id)
    return trace_model
