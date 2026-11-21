import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_api_health(client: AsyncClient):
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "HEALTHY"

@pytest.mark.asyncio
async def test_common_stations_api(client: AsyncClient):
    resp = await client.get("/api/stations/common?train1=12656&train2=12705")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    codes = [item["station_code"] for item in data]
    assert "MABD" in codes # Mahbubabad is shared!

@pytest.mark.asyncio
async def test_create_and_retrieve_race(client: AsyncClient):
    # Create race
    create_payload = {
        "train1_number": "12656",
        "train2_number": "12705",
        "destination_station_code": "MABD"
    }
    resp = await client.post("/api/races", json=create_payload)
    assert resp.status_code == 200
    race_summary = resp.json()
    race_id = race_summary["id"]
    assert race_id is not None
    assert race_summary["train1_number"] == "12656"
    assert race_summary["destination_station_code"] == "MABD"

    # Retrieve live race dashboard data
    race_resp = await client.get(f"/api/races/{race_id}")
    assert race_resp.status_code == 200
    race_data = race_resp.json()
    assert race_data["race_id"] == race_id
    assert race_data["destination_station_code"] == "MABD"
    assert race_data["leader"]["leader_train_number"] in ["12656", "12705"]
    assert race_data["train1"]["train_number"] == "12656"
    assert race_data["train2"]["train_number"] == "12705"
    assert race_data["train1"]["current_delay_min"] >= 0
    assert race_data["train2"]["current_delay_min"] >= 0

@pytest.mark.asyncio
async def test_create_invalid_race_destination_fails(client: AsyncClient):
    # Attempt race to a station NOT on the route of both trains
    invalid_payload = {
        "train1_number": "12656",
        "train2_number": "12705",
        "destination_station_code": "NDLS" # Neither train terminates/passes NDLS
    }
    resp = await client.post("/api/races", json=invalid_payload)
    assert resp.status_code == 400
    assert "not a valid common destination" in resp.json()["detail"]
