import json
from dataclasses import dataclass
from typing import List

# This file defines structure of the sensor data
# Response from http://tesla.iem.pw.edu.pl:9080/v2/monitor/1 is a blueprint for how the data looks
@dataclass
class Sensor:
    anomaly: bool
    id: int
    name: str
    value: int

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


@dataclass
class Trace:
    id: int
    name: str
    sensors: List[Sensor]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


@dataclass
class Reading:
    birthdate: int
    disabled: bool
    firstname: str
    id: int
    lastname: str
    trace: Trace

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
