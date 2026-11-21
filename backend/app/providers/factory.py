from app.config import settings
from app.providers.base import RailwayDataProvider
from app.providers.demo_provider import DemoRailwayDataProvider, STATIONS_DB
from app.providers.rapidapi_provider import RapidAPIRailwayProvider

_demo_provider_instance = DemoRailwayDataProvider()
_rapidapi_provider_instance = None

def get_railway_provider() -> RailwayDataProvider:
    """
    Factory function to get the configured RailwayDataProvider.
    Gracefully falls back to DemoRailwayDataProvider if RapidAPI is selected
    without valid credentials or when offline.
    """
    global _rapidapi_provider_instance
    provider_name = settings.RAILWAY_API_PROVIDER.lower().strip()

    if provider_name in ["rapidapi", "live"]:
        if settings.RAPIDAPI_KEY:
            if _rapidapi_provider_instance is None:
                _rapidapi_provider_instance = RapidAPIRailwayProvider(
                    api_key=settings.RAPIDAPI_KEY,
                    api_host=settings.RAPIDAPI_HOST
                )
            return _rapidapi_provider_instance
        else:
            # Fallback to demo when key is not provided
            return _demo_provider_instance

    return _demo_provider_instance

def get_station_metadata(code: str) -> dict:
    return STATIONS_DB.get(code.upper(), {
        "code": code.upper(),
        "name": code.upper(),
        "state": None,
        "lat": None,
        "lng": None
    })
