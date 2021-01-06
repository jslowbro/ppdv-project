import json
from tinydb import TinyDB, Query

from models import Reading
from models_marshaller import unmarshal_reading

# This file handles connecting to the database (writing and reading to file historic-readings.json)
# It breaks all the time so we'll be probably using a different database in the future

db = TinyDB('db/historic-readings.json', ensure_ascii=False)


def insert_reading(reading: Reading):
    reading_dict = json.loads(reading.toJSON())
    return get_table(reading.firstname, reading.lastname).insert(reading_dict)


def get_readings(first_name: str, last_name: str):
    reading = Query()
    ret = get_table(first_name, last_name).search((reading.firstname == first_name) & (reading.lastname == last_name))
    return [unmarshal_reading(d) for d in ret]


def get_table(first_name: str, last_name: str):
    return db.table(first_name + last_name)
