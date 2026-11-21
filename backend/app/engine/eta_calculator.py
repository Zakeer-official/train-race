from datetime import datetime, timedelta
from typing import Optional, List, Tuple
from app.schemas.train import TrainStopSchema

def parse_time_to_minutes(time_str: Optional[str], day_count: int = 1) -> Optional[int]:
    """
    Convert a timetable time string HH:MM and day_count into total minutes from start of journey day 1.
    """
    if not time_str or ":" not in time_str:
        return None
    try:
        parts = time_str.strip().split(":")
        hours = int(parts[0])
        minutes = int(parts[1])
        return (day_count - 1) * 24 * 60 + hours * 60 + minutes
    except Exception:
        return None

def minutes_to_time_str(total_minutes: int) -> str:
    """
    Convert total journey minutes into a clean display format, e.g. '02:14 (Day 2)'.
    """
    day = (total_minutes // (24 * 60)) + 1
    rem_min = total_minutes % (24 * 60)
    hours = rem_min // 60
    minutes = rem_min % 60
    if day > 1:
        return f"{hours:02d}:{minutes:02d} (Day {day})"
    return f"{hours:02d}:{minutes:02d}"

class ETACalculator:
    """
    Multi-level ETA Calculation Framework for Indian Railways.
    Computes:
    1. Timetable-derived ETA (scheduled arrival + current delay)
    2. Backend-estimated ETA (physics & station-sequence based, taking speed & intermediate halts into account)
    3. Final unified predicted ETA with confidence level
    """

    @staticmethod
    def calculate_timetable_derived_eta(
        scheduled_arrival: Optional[str],
        day_count: int,
        current_delay_min: int
    ) -> Tuple[str, int]:
        """
        Level 3 Fallback: Timetable time + current delay.
        """
        scheduled_minutes = parse_time_to_minutes(scheduled_arrival, day_count)
        if scheduled_minutes is None:
            return ("Unknown", 0)
        
        derived_minutes = scheduled_minutes + current_delay_min
        return (minutes_to_time_str(derived_minutes), derived_minutes)

    @staticmethod
    def calculate_backend_estimated_eta(
        all_stops: List[TrainStopSchema],
        current_station_code: str,
        destination_station_code: str,
        current_speed_kmh: float,
        current_delay_min: int,
        train_type: str = "SUPERFAST"
    ) -> Tuple[str, int, float, int]:
        """
        Level 2 Engine: Physics-based calculation incorporating remaining distance,
        cruising speed, intermediate halt durations, and observed delay propagation.
        Returns: (eta_str, total_minutes, remaining_distance_km, remaining_duration_min)
        """
        # Find index of current station and destination
        curr_idx = -1
        dest_idx = -1
        for i, s in enumerate(all_stops):
            if s.station_code == current_station_code:
                curr_idx = i
            if s.station_code == destination_station_code:
                dest_idx = i

        if dest_idx == -1:
            return ("Unknown", 0, 0.0, 0)

        # Scheduled destination arrival
        dest_stop = all_stops[dest_idx]
        dest_scheduled_min = parse_time_to_minutes(dest_stop.scheduled_arrival, dest_stop.day_count) or 0

        if curr_idx == -1 or curr_idx >= dest_idx:
            # Train is at or past destination or current station not in sequence
            derived_min = dest_scheduled_min + current_delay_min
            return (minutes_to_time_str(derived_min), derived_min, 0.0, 0)

        # Calculate remaining distance
        curr_stop = all_stops[curr_idx]
        rem_distance_km = max(0.0, dest_stop.distance_km - curr_stop.distance_km)
        
        # Calculate intermediate halts
        intermediate_stops = all_stops[curr_idx + 1:dest_idx]
        halt_time_min = len(intermediate_stops) * 3 # Average 3 minutes per intermediate station halt

        # Realistic cruise speed
        effective_speed = max(45.0, min(110.0, current_speed_kmh if current_speed_kmh > 30 else (75.0 if "RAJ" in train_type or "SHAT" in train_type else 65.0)))
        
        # Travel time in minutes
        travel_time_min = int((rem_distance_km / effective_speed) * 60) + halt_time_min
        
        # Estimated arrival = current scheduled time of current stop + current delay + travel time
        curr_sched_dep_min = parse_time_to_minutes(curr_stop.scheduled_departure or curr_stop.scheduled_arrival, curr_stop.day_count) or 0
        now_journey_min = curr_sched_dep_min + current_delay_min
        backend_predicted_min = now_journey_min + travel_time_min

        # Blend with timetable + delay to avoid extreme deviations
        timetable_min = dest_scheduled_min + current_delay_min
        blended_min = int(0.65 * backend_predicted_min + 0.35 * timetable_min)

        return (minutes_to_time_str(blended_min), blended_min, rem_distance_km, travel_time_min)

    @staticmethod
    def compute_confidence(
        data_freshness_sec: int,
        remaining_stops_count: int,
        has_live_speed: bool
    ) -> float:
        """
        Confidence formula based on:
        - Freshness of location data
        - Proximity to destination (fewer remaining stops = higher certainty)
        - Telemetry reliability (speed sensor active)
        """
        score = 0.95
        if data_freshness_sec > 300: # > 5 min
            score -= 0.15
        elif data_freshness_sec > 120: # > 2 min
            score -= 0.08
            
        if remaining_stops_count > 10:
            score -= 0.10
        elif remaining_stops_count > 5:
            score -= 0.05
            
        if not has_live_speed:
            score -= 0.07

        return max(0.40, min(0.98, round(score, 2)))
