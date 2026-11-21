import httpx
import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
from app.providers.base import RailwayDataProvider
from app.schemas.train import TrainInfo, TrainStopSchema, RunningStatusResponse

class RapidAPIRailwayProvider(RailwayDataProvider):
    """
    Production Railway Data Provider Adapter for Indian Railways via RapidAPI (e.g. irctc1 / railway-status).
    Features:
    - Retries with exponential backoff
    - Timeouts and robust error handling
    - Health monitoring and rate-limiting inspection
    """
    name = "RapidAPI Indian Railways"
    is_live = True

    def __init__(self, api_key: str, api_host: str = "irctc1.p.rapidapi.com"):
        self.api_key = api_key
        self.api_host = api_host
        self.base_url = f"https://{api_host}"
        self.timeout = httpx.Timeout(10.0, connect=5.0)

    def _headers(self) -> Dict[str, str]:
        return {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host,
            "Accept": "application/json"
        }

    async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("RapidAPI Key is not configured.")

        url = f"{self.base_url}/{endpoint}"
        max_retries = 3
        backoff = 1.0

        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    resp = await client.get(url, headers=self._headers(), params=params)
                    if resp.status_code == 429:
                        raise httpx.HTTPStatusError("Rate limit exceeded", request=resp.request, response=resp)
                    resp.raise_for_status()
                    return resp.json()
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                if attempt == max_retries - 1:
                    raise e
                await asyncio.sleep(backoff)
                backoff *= 2.0
        return {}

    async def search_train(self, query: str) -> List[TrainInfo]:
        try:
            data = await self._make_request("api/v1/searchTrain", {"query": query})
            trains_data = data.get("data", [])
            results = []
            for item in trains_data:
                results.append(
                    TrainInfo(
                        number=str(item.get("train_number", "")),
                        name=item.get("train_name", ""),
                        train_type=item.get("train_type", "SUPERFAST"),
                        source_station_code=item.get("from_station_code", ""),
                        dest_station_code=item.get("to_station_code", ""),
                    )
                )
            return results
        except Exception:
            return []

    async def get_train_details(self, train_number: str) -> Optional[TrainInfo]:
        results = await self.search_train(train_number)
        for t in results:
            if t.number == train_number:
                return t
        return None

    async def get_train_route(self, train_number: str) -> List[TrainStopSchema]:
        try:
            data = await self._make_request("api/v1/getTrainSchedule", {"trainNo": train_number})
            schedule = data.get("data", {}).get("schedule", [])
            stops = []
            for s in schedule:
                stops.append(
                    TrainStopSchema(
                        sequence=int(s.get("station_order", 0)),
                        station_code=s.get("station_code", ""),
                        station_name=s.get("station_name", ""),
                        scheduled_arrival=s.get("arrival_time"),
                        scheduled_departure=s.get("departure_time"),
                        distance_km=float(s.get("distance_from_source", 0.0)),
                        day_count=int(s.get("day_count", 1))
                    )
                )
            return stops
        except Exception:
            return []

    async def get_running_status(self, train_number: str, destination_station: Optional[str] = None) -> RunningStatusResponse:
        # Standard endpoint for live running status
        today_str = datetime.utcnow().strftime("%Y%m%d")
        data = await self._make_request("api/v1/liveTrainStatus", {
            "trainNo": train_number,
            "startDay": "0"
        })
        payload = data.get("data", {})
        curr_code = payload.get("current_station_code", "UNKNOWN")
        curr_name = payload.get("current_station_name", curr_code)
        delay_min = int(payload.get("delay", 0))
        speed = float(payload.get("speed", 0.0))

        return RunningStatusResponse(
            train_number=train_number,
            train_name=payload.get("train_name", f"Train {train_number}"),
            current_station_code=curr_code,
            current_station_name=curr_name,
            current_status_message=payload.get("status_as_of", f"Running with {delay_min}m delay"),
            delay_minutes=delay_min,
            speed_kmh=speed,
            distance_from_source_km=float(payload.get("distance_from_source", 0.0)),
            total_distance_km=float(payload.get("total_distance", 0.0)),
            distance_to_destination_km=0.0,
            last_updated_time=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            data_source=f"RapidAPI ({self.api_host})",
            is_simulated=False,
            data_freshness_seconds=0
        )

    async def get_provider_health(self) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "provider": self.name,
                "status": "UNCONFIGURED",
                "latency_ms": 0,
                "is_live": True,
                "message": "RapidAPI key not provided. Running in Demo fallback mode."
            }
        t0 = datetime.utcnow()
        try:
            await self._make_request("api/v1/searchTrain", {"query": "12656"})
            latency = (datetime.utcnow() - t0).total_seconds() * 1000
            return {
                "provider": self.name,
                "status": "HEALTHY",
                "latency_ms": round(latency, 1),
                "is_live": True,
                "message": "RapidAPI connection healthy."
            }
        except Exception as e:
            return {
                "provider": self.name,
                "status": "ERROR",
                "latency_ms": 0,
                "is_live": True,
                "message": str(e)
            }
