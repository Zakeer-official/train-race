import pytest
from app.engine.eta_calculator import ETACalculator, parse_time_to_minutes, minutes_to_time_str
from app.engine.comparison import TrainComparisonEngine
from app.schemas.train import RunningStatusResponse, TrainStopSchema
from app.schemas.comparison import PredictionSnapshotItem

def test_time_parsing_and_conversion():
    # Day 1: 06:35
    m1 = parse_time_to_minutes("06:35", day_count=1)
    assert m1 == 6 * 60 + 35

    # Day 2: 02:14 (Overnight journey handling)
    m2 = parse_time_to_minutes("02:14", day_count=2)
    assert m2 == 24 * 60 + 2 * 60 + 14

    # Format check
    assert minutes_to_time_str(m2) == "02:14 (Day 2)"
    assert minutes_to_time_str(m1) == "06:35"

def test_timetable_derived_eta():
    eta_str, eta_min = ETACalculator.calculate_timetable_derived_eta(
        scheduled_arrival="14:00",
        day_count=1,
        current_delay_min=30
    )
    assert eta_str == "14:30"
    assert eta_min == 14 * 60 + 30

def test_backend_estimated_eta():
    stops = [
        TrainStopSchema(sequence=1, station_code="ST1", station_name="Start", scheduled_departure="08:00", distance_km=0.0, day_count=1),
        TrainStopSchema(sequence=2, station_code="MID", station_name="Mid", scheduled_arrival="09:00", scheduled_departure="09:05", distance_km=60.0, day_count=1),
        TrainStopSchema(sequence=3, station_code="DEST", station_name="End", scheduled_arrival="10:00", distance_km=120.0, day_count=1)
    ]
    eta_str, eta_min, rem_dist, rem_dur = ETACalculator.calculate_backend_estimated_eta(
        all_stops=stops,
        current_station_code="MID",
        destination_station_code="DEST",
        current_speed_kmh=60.0,
        current_delay_min=10,
        train_type="SUPERFAST"
    )
    assert rem_dist == 60.0
    assert rem_dur > 0
    assert eta_min > 0
    assert ":" in eta_str

def test_confidence_score_calculation():
    # High confidence: fresh data, few remaining stops, active speed
    high = ETACalculator.compute_confidence(data_freshness_sec=10, remaining_stops_count=2, has_live_speed=True)
    assert high >= 0.90

    # Degraded confidence: stale data, many stops
    low = ETACalculator.compute_confidence(data_freshness_sec=400, remaining_stops_count=15, has_live_speed=False)
    assert low < high
