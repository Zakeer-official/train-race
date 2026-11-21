from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.schemas.train import TrainInfo, TrainStopSchema, RunningStatusResponse

class RailwayDataProvider(ABC):
    """
    Abstract interface for railway data providers (NTES, RailRadar, RapidAPI, Demo).
    Guarantees provider-independence across the application.
    """
    name: str = "BaseProvider"
    is_live: bool = False

    @abstractmethod
    async def search_train(self, query: str) -> List[TrainInfo]:
        """Search trains by number or name."""
        pass

    @abstractmethod
    async def get_train_details(self, train_number: str) -> Optional[TrainInfo]:
        """Get train metadata including source and destination."""
        pass

    @abstractmethod
    async def get_train_route(self, train_number: str) -> List[TrainStopSchema]:
        """Get ordered list of stops with scheduled times and distances."""
        pass

    @abstractmethod
    async def get_running_status(self, train_number: str, destination_station: Optional[str] = None) -> RunningStatusResponse:
        """Get live running status, current station, delay, speed and coordinates."""
        pass

    @abstractmethod
    async def get_provider_health(self) -> Dict[str, Any]:
        """Check provider health, latency, and quota/availability."""
        pass
