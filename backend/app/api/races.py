from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
import json
import asyncio

from app.database import get_db
from app.models.race import RaceSession
from app.schemas.race import RaceCreateRequest, RaceSummary
from app.schemas.comparison import LiveRaceComparison
from app.services.race_service import RaceService
from app.config import settings

router = APIRouter(prefix="/api/races", tags=["Races"])

@router.post("", response_model=RaceSummary)
async def create_race(req: RaceCreateRequest, db: AsyncSession = Depends(get_db)):
    try:
        race = await RaceService.create_race(
            db=db,
            train1_number=req.train1_number,
            train2_number=req.train2_number,
            dest_station_code=req.destination_station_code
        )
        return RaceSummary(
            id=race.id,
            train1_number=race.train1_number,
            train2_number=race.train2_number,
            destination_station_code=race.destination_station_code,
            status=race.status,
            is_demo=race.is_demo,
            created_at=race.created_at.isoformat(),
            share_url=f"{settings.BASE_URL}/race/{race.id}"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{race_id}", response_model=LiveRaceComparison)
async def get_race(race_id: str, db: AsyncSession = Depends(get_db)):
    try:
        return await RaceService.get_live_race_data(db, race_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Race session {race_id} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[RaceSummary])
async def list_recent_races(db: AsyncSession = Depends(get_db)):
    stmt = select(RaceSession).order_by(desc(RaceSession.created_at)).limit(10)
    res = await db.execute(stmt)
    races = res.scalars().all()
    return [
        RaceSummary(
            id=r.id,
            train1_number=r.train1_number,
            train2_number=r.train2_number,
            destination_station_code=r.destination_station_code,
            status=r.status,
            is_demo=r.is_demo,
            created_at=r.created_at.isoformat(),
            share_url=f"{settings.BASE_URL}/race/{r.id}"
        )
        for r in races
    ]

@router.get("/{race_id}/live")
async def live_race_sse(race_id: str, db: AsyncSession = Depends(get_db)):
    """
    Server-Sent Events (SSE) stream delivering real-time race updates directly to the client.
    """
    async def event_generator():
        while True:
            try:
                data = await RaceService.get_live_race_data(db, race_id)
                payload = data.model_dump_json()
                yield f"data: {payload}\n\n"
            except Exception as e:
                err_data = json.dumps({"error": str(e)})
                yield f"event: error\ndata: {err_data}\n\n"
            await asyncio.sleep(15) # Push every 15s

    return StreamingResponse(event_generator(), media_type="text/event-stream")
