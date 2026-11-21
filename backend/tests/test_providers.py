import pytest
from app.providers.demo_provider import DemoRailwayDataProvider
from app.engine.comparison import TrainComparisonEngine

@pytest.mark.asyncio
async def test_demo_provider_search_and_route():
    provider = DemoRailwayDataProvider()
    trains = await provider.search_train("12656")
    assert len(trains) > 0
    assert trains[0].number == "12656"

    route = await provider.get_train_route("12656")
    assert len(route) >= 10
    station_codes = [s.station_code for s in route]
    assert "MABD" in station_codes
    assert "WL" in station_codes

@pytest.mark.asyncio
async def test_head_to_head_comparison_winner_selection():
    provider = DemoRailwayDataProvider()
    status1 = await provider.get_running_status("12656", destination_station="MABD")
    status2 = await provider.get_running_status("12705", destination_station="MABD")

    comparison = TrainComparisonEngine.compare_races(
        race_id="test_race_123",
        dest_station_code="MABD",
        status1=status1,
        status2=status2
    )

    assert comparison.race_id == "test_race_123"
    assert comparison.destination_station_code == "MABD"
    assert comparison.leader.leader_train_number in ["12656", "12705"]
    assert comparison.eta_gap_minutes >= 0
    assert len(comparison.leader.summary_message) > 0
    assert comparison.train1.confidence_score > 0.5
