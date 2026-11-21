from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.providers.factory import STATIONS_DB
from app.schemas.race import CommonStationOption
from app.services.race_service import RaceService

router = APIRouter(prefix="/api/stations", tags=["Stations"])

@router.get("/search")
async def search_stations(q: str = Query(..., min_length=2)):
    query = q.strip().upper()
    matches = []
    for code, meta in STATIONS_DB.items():
        if query in code or query in meta["name"].upper():
            matches.append(meta)
    return matches[:15]

@router.get("/common", response_model=List[CommonStationOption])
async def get_common_stations(
    train1: str = Query(..., description="Train 1 number"),
    train2: str = Query(..., description="Train 2 number")
):
    common = await RaceService.find_common_stations(train1, train2)
    return common
