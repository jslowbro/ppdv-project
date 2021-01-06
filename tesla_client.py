import requests

from models import Reading
from models_marshaller import unmarshal_reading


# This file is used for accessing the API that we're meant to work with
url = "http://tesla.iem.pw.edu.pl:9080/v2/monitor/"


def get_patient_reading(reading_id: int) -> Reading:
    response = requests.get(url + str(reading_id))
    reading = unmarshal_reading(response.json())
    return reading
