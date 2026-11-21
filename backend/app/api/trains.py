from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.providers.factory import get_railway_provider
from app.schemas.train import TrainInfo, TrainStopSchema, RunningStatusResponse

router = APIRouter(prefix="/api/trains", tags=["Trains"])

@router.get("/search", response_model=List[TrainInfo])
async def search_trains(q: str = Query(..., min_length=2, description="Train number or name prefix")):
    provider = get_railway_provider()
    return await provider.search_train(q)

@router.get("/{train_number}", response_model=TrainInfo)
async def get_train(train_number: str):
    provider = get_railway_provider()
    details = await provider.get_train_details(train_number)
    if not details:
        raise HTTPException(status_code=404, detail=f"Train {train_number} not found.")
    return details

@router.get("/{train_number}/route", response_model=List[TrainStopSchema])
async def get_train_route(train_number: str):
    provider = get_railway_provider()
    stops = await provider.get_train_route(train_number)
    if not stops:
        raise HTTPException(status_code=404, detail=f"Route for train {train_number} not found.")
    return stops

@router.get("/{train_number}/status", response_model=RunningStatusResponse)
async def get_running_status(train_number: str, destination: Optional[str] = None):
    provider = get_railway_provider()
    try:
        return await provider.get_running_status(train_number, destination)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
