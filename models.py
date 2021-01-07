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


@dataclass
class TraceModel:
    trace_id: int
    patient_id: int
    l0: int
    l0a: bool
    l1: int
    l1a: bool
    l2: int
    l2a: bool
    r0: int
    r0a: bool
    r1: int
    r1a: bool
    r2: int
    r2a: bool

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
