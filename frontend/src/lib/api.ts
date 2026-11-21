import {
  LiveRaceComparison,
  RaceSummary,
  CommonStationOption,
  TrainInfo,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchRaceData(raceId: string): Promise<LiveRaceComparison> {
  const res = await fetch(`${API_BASE}/api/races/${raceId}`, {
    cache: "no-store",
  });
  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Failed to load race: ${errorText}`);
  }
  return res.json();
}

export async function createRace(
  train1: string,
  train2: string,
  destination: string
): Promise<RaceSummary> {
  const res = await fetch(`${API_BASE}/api/races`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      train1_number: train1,
      train2_number: train2,
      destination_station_code: destination,
    }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Failed to create race.");
  }
  return res.json();
}

export async function fetchCommonStations(
  train1: string,
  train2: string
): Promise<CommonStationOption[]> {
  const res = await fetch(
    `${API_BASE}/api/stations/common?train1=${encodeURIComponent(
      train1
    )}&train2=${encodeURIComponent(train2)}`
  );
  if (!res.ok) {
    return [];
  }
  return res.json();
}

export async function searchTrains(query: string): Promise<TrainInfo[]> {
  if (!query || query.length < 2) return [];
  const res = await fetch(
    `${API_BASE}/api/trains/search?q=${encodeURIComponent(query)}`
  );
  if (!res.ok) return [];
  return res.json();
}

export async function fetchRecentRaces(): Promise<RaceSummary[]> {
  const res = await fetch(`${API_BASE}/api/races`, { cache: "no-store" });
  if (!res.ok) return [];
  return res.json();
}

export async function fetchProviderHealth(): Promise<any> {
  const res = await fetch(`${API_BASE}/api/health/providers`, {
    cache: "no-store",
  });
  if (!res.ok) return { status: "OFFLINE" };
  return res.json();
}
