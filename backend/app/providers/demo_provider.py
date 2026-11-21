import asyncio
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any
from app.providers.base import RailwayDataProvider
from app.schemas.train import TrainInfo, TrainStopSchema, RunningStatusResponse

# Real station dictionary with accurate GPS coordinates for Leaflet map & distance calculations
STATIONS_DB: Dict[str, Dict[str, Any]] = {
    "ADI": {"code": "ADI", "name": "Ahmedabad Junction", "state": "Gujarat", "lat": 23.0225, "lng": 72.5714},
    "ST": {"code": "ST", "name": "Surat", "state": "Gujarat", "lat": 21.1702, "lng": 72.8311},
    "BSL": {"code": "BSL", "name": "Bhusaval Junction", "state": "Maharashtra", "lat": 21.0500, "lng": 75.7833},
    "BD": {"code": "BD", "name": "Badnera Junction", "state": "Maharashtra", "lat": 20.8667, "lng": 77.7333},
    "WR": {"code": "WR", "name": "Wardha Junction", "state": "Maharashtra", "lat": 20.7453, "lng": 78.6022},
    "BPQ": {"code": "BPQ", "name": "Balharshah Junction", "state": "Maharashtra", "lat": 19.8515, "lng": 79.3510},
    "SKZR": {"code": "SKZR", "name": "Sirpur Kaghaznagar", "state": "Telangana", "lat": 19.3411, "lng": 79.4939},
    "RDM": {"code": "RDM", "name": "Ramagundam", "state": "Telangana", "lat": 18.7619, "lng": 79.4754},
    "KZJ": {"code": "KZJ", "name": "Kazipet Junction", "state": "Telangana", "lat": 17.9787, "lng": 79.5255},
    "WL": {"code": "WL", "name": "Warangal", "state": "Telangana", "lat": 17.9689, "lng": 79.5941},
    "MABD": {"code": "MABD", "name": "Mahbubabad", "state": "Telangana", "lat": 17.5986, "lng": 80.0033},
    "KMT": {"code": "KMT", "name": "Khammam", "state": "Telangana", "lat": 17.2472, "lng": 80.1514},
    "BZA": {"code": "BZA", "name": "Vijayawada Junction", "state": "Andhra Pradesh", "lat": 16.5062, "lng": 80.6480},
    "MAS": {"code": "MAS", "name": "MGR Chennai Central", "state": "Tamil Nadu", "lat": 13.0827, "lng": 80.2707},
    
    # Gouthami / Krishna route (Secunderabad - MABD - BZA)
    "SC": {"code": "SC", "name": "Secunderabad Junction", "state": "Telangana", "lat": 17.4334, "lng": 78.5015},
    "BG": {"code": "BG", "name": "Bhongir", "state": "Telangana", "lat": 17.5111, "lng": 78.8889},
    "ZN": {"code": "ZN", "name": "Jangaon", "state": "Telangana", "lat": 17.7239, "lng": 79.1624},
    "DKJ": {"code": "DKJ", "name": "Dornakal Junction", "state": "Telangana", "lat": 17.4475, "lng": 80.1481},
    "MDR": {"code": "MDR", "name": "Madhira", "state": "Telangana", "lat": 16.9200, "lng": 80.3600},
    "GNT": {"code": "GNT", "name": "Guntur Junction", "state": "Andhra Pradesh", "lat": 16.3067, "lng": 80.4365},

    # Rajdhani Route (Mumbai - Delhi)
    "MMCT": {"code": "MMCT", "name": "Mumbai Central", "state": "Maharashtra", "lat": 18.9696, "lng": 72.8194},
    "BRC": {"code": "BRC", "name": "Vadodara Junction", "state": "Gujarat", "lat": 22.3107, "lng": 73.1812},
    "RTM": {"code": "RTM", "name": "Ratlam Junction", "state": "Madhya Pradesh", "lat": 23.3344, "lng": 75.0372},
    "KOTA": {"code": "KOTA", "name": "Kota Junction", "state": "Rajasthan", "lat": 25.2138, "lng": 75.8648},
    "MTJ": {"code": "MTJ", "name": "Mathura Junction", "state": "Uttar Pradesh", "lat": 27.4924, "lng": 77.6737},
    "NDLS": {"code": "NDLS", "name": "New Delhi", "state": "Delhi", "lat": 28.6431, "lng": 77.2197},
    "AGC": {"code": "AGC", "name": "Agra Cantt", "state": "Uttar Pradesh", "lat": 27.1593, "lng": 78.0069},
    "GWL": {"code": "GWL", "name": "Gwalior Junction", "state": "Madhya Pradesh", "lat": 26.2183, "lng": 78.1828},
    "VGLJ": {"code": "VGLJ", "name": "VGL Jhansi Junction", "state": "Uttar Pradesh", "lat": 25.4484, "lng": 78.5685},
    "BPL": {"code": "BPL", "name": "Bhopal Junction", "state": "Madhya Pradesh", "lat": 23.2599, "lng": 77.4126},
}

TRAINS_DATABASE: Dict[str, Dict[str, Any]] = {
    "12656": {
        "number": "12656",
        "name": "Navjeevan Superfast Express",
        "train_type": "SUPERFAST",
        "source": "ADI",
        "destination": "MAS",
        "stops": [
            {"code": "ADI", "seq": 1, "arr": None, "dep": "06:35", "dist": 0.0, "day": 1},
            {"code": "ST", "seq": 2, "arr": "10:10", "dep": "10:15", "dist": 230.0, "day": 1},
            {"code": "BSL", "seq": 3, "arr": "15:20", "dep": "15:25", "dist": 565.0, "day": 1},
            {"code": "BD", "seq": 4, "arr": "18:00", "dep": "18:05", "dist": 783.0, "day": 1},
            {"code": "WR", "seq": 5, "arr": "19:18", "dep": "19:20", "dist": 878.0, "day": 1},
            {"code": "BPQ", "seq": 6, "arr": "21:40", "dep": "21:45", "dist": 1011.0, "day": 1},
            {"code": "SKZR", "seq": 7, "arr": "22:38", "dep": "22:40", "dist": 1081.0, "day": 1},
            {"code": "RDM", "seq": 8, "arr": "23:29", "dep": "23:30", "dist": 1153.0, "day": 1},
            {"code": "KZJ", "seq": 9, "arr": "01:03", "dep": "01:05", "dist": 1246.0, "day": 2},
            {"code": "WL", "seq": 10, "arr": "01:18", "dep": "01:20", "dist": 1256.0, "day": 2},
            {"code": "MABD", "seq": 11, "arr": "02:14", "dep": "02:15", "dist": 1316.0, "day": 2},
            {"code": "KMT", "seq": 12, "arr": "02:49", "dep": "02:50", "dist": 1363.0, "day": 2},
            {"code": "BZA", "seq": 13, "arr": "04:45", "dep": "04:55", "dist": 1463.0, "day": 2},
            {"code": "MAS", "seq": 14, "arr": "11:45", "dep": None, "dist": 1894.0, "day": 2},
        ],
        "default_active_stop_idx": 9, # Warangal
        "base_delay_min": 18,
        "base_speed": 82.0
    },
    "12705": {
        "number": "12705",
        "name": "Gouthami Superfast Express",
        "train_type": "SUPERFAST",
        "source": "SC",
        "destination": "GNT",
        "stops": [
            {"code": "SC", "seq": 1, "arr": None, "dep": "23:25", "dist": 0.0, "day": 1},
            {"code": "BG", "seq": 2, "arr": "00:04", "dep": "00:05", "dist": 46.0, "day": 2},
            {"code": "ZN", "seq": 3, "arr": "00:34", "dep": "00:35", "dist": 84.0, "day": 2},
            {"code": "KZJ", "seq": 4, "arr": "01:28", "dep": "01:30", "dist": 132.0, "day": 2},
            {"code": "WL", "seq": 5, "arr": "01:43", "dep": "01:45", "dist": 142.0, "day": 2},
            {"code": "MABD", "seq": 6, "arr": "02:38", "dep": "02:39", "dist": 202.0, "day": 2},
            {"code": "DKJ", "seq": 7, "arr": "03:04", "dep": "03:05", "dist": 227.0, "day": 2},
            {"code": "KMT", "seq": 8, "arr": "03:24", "dep": "03:25", "dist": 249.0, "day": 2},
            {"code": "MDR", "seq": 9, "arr": "03:59", "dep": "04:00", "dist": 294.0, "day": 2},
            {"code": "BZA", "seq": 10, "arr": "05:15", "dep": "05:25", "dist": 349.0, "day": 2},
            {"code": "GNT", "seq": 11, "arr": "06:30", "dep": None, "dist": 381.0, "day": 2},
        ],
        "default_active_stop_idx": 3, # Kazipet
        "base_delay_min": 7,
        "base_speed": 74.0
    },
    "12951": {
        "number": "12951",
        "name": "Mumbai Rajdhani Express",
        "train_type": "RAJDHANI",
        "source": "MMCT",
        "destination": "NDLS",
        "stops": [
            {"code": "MMCT", "seq": 1, "arr": None, "dep": "17:00", "dist": 0.0, "day": 1},
            {"code": "ST", "seq": 2, "arr": "19:43", "dep": "19:48", "dist": 263.0, "day": 1},
            {"code": "BRC", "seq": 3, "arr": "21:06", "dep": "21:16", "dist": 392.0, "day": 1},
            {"code": "RTM", "seq": 4, "arr": "00:25", "dep": "00:28", "dist": 653.0, "day": 2},
            {"code": "KOTA", "seq": 5, "arr": "03:15", "dep": "03:20", "dist": 920.0, "day": 2},
            {"code": "MTJ", "seq": 6, "arr": "06:40", "dep": "06:42", "dist": 1243.0, "day": 2},
            {"code": "NDLS", "seq": 7, "arr": "08:32", "dep": None, "dist": 1384.0, "day": 2},
        ],
        "default_active_stop_idx": 4,
        "base_delay_min": 5,
        "base_speed": 98.0
    },
    "12953": {
        "number": "12953",
        "name": "August Kranti Rajdhani Express",
        "train_type": "RAJDHANI",
        "source": "MMCT",
        "destination": "NDLS",
        "stops": [
            {"code": "MMCT", "seq": 1, "arr": None, "dep": "17:10", "dist": 0.0, "day": 1},
            {"code": "ST", "seq": 2, "arr": "19:55", "dep": "20:00", "dist": 263.0, "day": 1},
            {"code": "BRC", "seq": 3, "arr": "21:20", "dep": "21:30", "dist": 392.0, "day": 1},
            {"code": "RTM", "seq": 4, "arr": "00:45", "dep": "00:48", "dist": 653.0, "day": 2},
            {"code": "KOTA", "seq": 5, "arr": "03:40", "dep": "03:45", "dist": 920.0, "day": 2},
            {"code": "MTJ", "seq": 6, "arr": "07:10", "dep": "07:12", "dist": 1243.0, "day": 2},
            {"code": "NDLS", "seq": 7, "arr": "09:43", "dep": None, "dist": 1384.0, "day": 2},
        ],
        "default_active_stop_idx": 4,
        "base_delay_min": 12,
        "base_speed": 94.0
    }
}

class DemoRailwayDataProvider(RailwayDataProvider):
    """
    Rich Realistic Demo Provider for Indian Railway head-to-head train races.
    Simulates live telemetry, realistic delays, GPS coordinates, and route progress.
    Explicitly labeled as simulated data.
    """
    name = "DemoProvider (Synthetic Indian Railways Live Simulation)"
    is_live = False

    def __init__(self):
        # In-memory runtime offsets to simulate live train movement and delay fluctuations over time
        self._start_time = datetime.now(timezone.utc)

    async def search_train(self, query: str) -> List[TrainInfo]:
        q = query.strip().upper()
        results = []
        for t_num, t_data in TRAINS_DATABASE.items():
            if q in t_num or q in t_data["name"].upper():
                src_code = t_data["source"]
                dst_code = t_data["destination"]
                results.append(
                    TrainInfo(
                        number=t_num,
                        name=t_data["name"],
                        train_type=t_data["train_type"],
                        source_station_code=src_code,
                        dest_station_code=dst_code,
                        source_station_name=STATIONS_DB.get(src_code, {}).get("name", src_code),
                        dest_station_name=STATIONS_DB.get(dst_code, {}).get("name", dst_code)
                    )
                )
        return results

    async def get_train_details(self, train_number: str) -> Optional[TrainInfo]:
        t_num = train_number.strip()
        if t_num not in TRAINS_DATABASE:
            return None
        t_data = TRAINS_DATABASE[t_num]
        src_code = t_data["source"]
        dst_code = t_data["destination"]
        return TrainInfo(
            number=t_num,
            name=t_data["name"],
            train_type=t_data["train_type"],
            source_station_code=src_code,
            dest_station_code=dst_code,
            source_station_name=STATIONS_DB.get(src_code, {}).get("name", src_code),
            dest_station_name=STATIONS_DB.get(dst_code, {}).get("name", dst_code)
        )

    async def get_train_route(self, train_number: str) -> List[TrainStopSchema]:
        t_num = train_number.strip()
        if t_num not in TRAINS_DATABASE:
            return []
        
        stops_raw = TRAINS_DATABASE[t_num]["stops"]
        stops = []
        for s in stops_raw:
            code = s["code"]
            st_info = STATIONS_DB.get(code, {})
            name = st_info.get("name", code)
            stops.append(
                TrainStopSchema(
                    sequence=s["seq"],
                    station_code=code,
                    station_name=name,
                    scheduled_arrival=s["arr"],
                    scheduled_departure=s["dep"],
                    distance_km=s["dist"],
                    day_count=s["day"]
                )
            )
        return stops

    async def get_running_status(self, train_number: str, destination_station: Optional[str] = None) -> RunningStatusResponse:
        t_num = train_number.strip()
        if t_num not in TRAINS_DATABASE:
            raise ValueError(f"Train {train_number} not found in provider database.")

        t_data = TRAINS_DATABASE[t_num]
        stops_raw = t_data["stops"]
        total_stops = len(stops_raw)
        
        # Time-based elapsed seconds to simulate realistic live movement
        elapsed_sec = int((datetime.now(timezone.utc) - self._start_time).total_seconds())
        # Slight sinusoidal fluctuation for speed and delay
        cycle = (elapsed_sec // 15) % 10 # advances every 15s
        
        base_delay = t_data["base_delay_min"]
        # In race 12656 vs 12705:
        # 12656 starts ahead, but may encounter minor yellow signal delay while 12705 catches up!
        if t_num == "12656":
            sim_delay = max(5, base_delay + (cycle % 4) - 2)
            sim_speed = t_data["base_speed"] + (cycle % 5) * 2 - 4
        else:
            sim_delay = max(0, base_delay - (cycle % 3) + 1)
            sim_speed = t_data["base_speed"] + (cycle % 6) * 2 - 3
        
        active_idx = min(total_stops - 2, t_data["default_active_stop_idx"] + (elapsed_sec // 900))
        curr_stop_raw = stops_raw[active_idx]
        curr_code = curr_stop_raw["code"]
        curr_st = STATIONS_DB.get(curr_code, {"name": curr_code, "lat": 17.5, "lng": 79.5})
        
        # Construct all stops with departure/delay state
        all_stops = []
        for i, s in enumerate(stops_raw):
            code = s["code"]
            st_meta = STATIONS_DB.get(code, {})
            has_dep = i < active_idx
            is_curr = i == active_idx
            
            # Simulated actual arrival/departure
            arr_delay = sim_delay if i >= active_idx else max(0, sim_delay - 5)
            dep_delay = sim_delay if i >= active_idx else max(0, sim_delay - 4)
            
            all_stops.append(
                TrainStopSchema(
                    sequence=s["seq"],
                    station_code=code,
                    station_name=st_meta.get("name", code),
                    scheduled_arrival=s["arr"],
                    scheduled_departure=s["dep"],
                    delay_arrival_min=arr_delay,
                    delay_departure_min=dep_delay,
                    distance_km=s["dist"],
                    day_count=s["day"],
                    has_departed=has_dep,
                    is_current=is_curr
                )
            )

        upcoming_stops = all_stops[active_idx:]
        
        # Total and remaining distance
        tot_dist = stops_raw[-1]["dist"]
        curr_dist = curr_stop_raw["dist"]
        
        dest_dist = tot_dist
        if destination_station:
            for s in stops_raw:
                if s["code"] == destination_station:
                    dest_dist = s["dist"]
                    break
        
        dist_to_dest = max(0.0, dest_dist - curr_dist)

        return RunningStatusResponse(
            train_number=t_num,
            train_name=t_data["name"],
            current_station_code=curr_code,
            current_station_name=curr_st.get("name", curr_code),
            current_status_message=f"Departed {curr_st.get('name', curr_code)} with {sim_delay} min delay. Cruising at {int(sim_speed)} km/h.",
            delay_minutes=sim_delay,
            speed_kmh=round(sim_speed, 1),
            distance_from_source_km=curr_dist,
            total_distance_km=tot_dist,
            distance_to_destination_km=round(dist_to_dest, 1),
            last_updated_time=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            data_source="DEMO_SIMULATION (Synthetic Indian Railways Live Feed)",
            is_simulated=True,
            data_freshness_seconds=min(30, elapsed_sec % 45),
            current_lat=curr_st.get("lat"),
            current_lng=curr_st.get("lng"),
            upcoming_stops=upcoming_stops,
            all_stops=all_stops
        )

    async def get_provider_health(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "status": "HEALTHY",
            "latency_ms": 1.5,
            "is_live": False,
            "quota_remaining": "UNLIMITED",
            "message": "Demo simulation provider operational."
        }
