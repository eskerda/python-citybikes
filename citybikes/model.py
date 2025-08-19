from dataclasses import dataclass, fields, field
from typing import Optional

class AllowExtra:
    @classmethod
    def from_dict(cls, data):
        valid_keys = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered)

@dataclass
class Station(AllowExtra):
    id: str
    name: str
    latitude: float
    longitude: float
    extra: dict
    free_bikes: Optional[int] = None
    empty_slots: Optional[int] = None


@dataclass
class Location:
    latitude: float
    longitude: float
    city: str
    country: str

@dataclass
class Network(AllowExtra):
    id: str
    name: str
    location: Location
    href: str
    stations: list[Station] = field(default_factory=list)

    def __post_init__(self):
        self.stations = [Station.from_dict(s) for s in self.stations]
        self.location = Location(** self.location)
