from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.comparison import LiveRaceComparison

class RaceCreateRequest(BaseModel):
    train1_number: str = Field(..., description="First train number e.g. 12656")
    train2_number: str = Field(..., description="Second train number e.g. 12705")
    destination_station_code: str = Field(..., description="Common destination station code e.g. MABD")

class RaceSummary(BaseModel):
    id: str
    train1_number: str
    train2_number: str
    destination_station_code: str
    status: str
    is_demo: bool
    created_at: str
    share_url: str

class CommonStationOption(BaseModel):
    station_code: str
    station_name: str
    train1_sequence: int
    train2_sequence: int
    train1_scheduled_arrival: Optional[str] = None
    train2_scheduled_arrival: Optional[str] = None
