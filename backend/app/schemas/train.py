from pydantic import BaseModel, Field
from typing import List, Optional

class StationBase(BaseModel):
    code: str
    name: str
    state: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

class TrainStopSchema(BaseModel):
    sequence: int
    station_code: str
    station_name: str
    scheduled_arrival: Optional[str] = None
    scheduled_departure: Optional[str] = None
    actual_arrival: Optional[str] = None
    actual_departure: Optional[str] = None
    delay_arrival_min: int = 0
    delay_departure_min: int = 0
    distance_km: float = 0.0
    day_count: int = 1
    has_departed: bool = False
    is_current: bool = False

class TrainInfo(BaseModel):
    number: str
    name: str
    train_type: str = "SUPERFAST"
    source_station_code: str
    dest_station_code: str
    source_station_name: Optional[str] = None
    dest_station_name: Optional[str] = None

class TrainRouteResponse(BaseModel):
    train: TrainInfo
    stops: List[TrainStopSchema]

class RunningStatusResponse(BaseModel):
    train_number: str
    train_name: str
    current_station_code: str
    current_station_name: str
    current_status_message: str
    delay_minutes: int
    speed_kmh: float = 0.0
    distance_from_source_km: float = 0.0
    total_distance_km: float = 0.0
    distance_to_destination_km: float = 0.0
    last_updated_time: str
    data_source: str
    is_simulated: bool = False
    data_freshness_seconds: int = 0
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    upcoming_stops: List[TrainStopSchema] = []
    all_stops: List[TrainStopSchema] = []
