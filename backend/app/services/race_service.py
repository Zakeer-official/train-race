import asyncio
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.race import RaceSession, PredictionSnapshot, LeadChange
from app.models.station import Station
from app.providers.factory import get_railway_provider, STATIONS_DB
from app.engine.comparison import TrainComparisonEngine
from app.schemas.comparison import LiveRaceComparison, PredictionSnapshotItem, LeadChangeItem
from app.schemas.race import CommonStationOption
from app.services.cache import cache

class RaceService:
    """
    Service responsible for race creation, validation, live calculation,
    lead-change detection, and snapshot persistence.
    """

    @staticmethod
    async def find_common_stations(train1_number: str, train2_number: str) -> List[CommonStationOption]:
        provider = get_railway_provider()
        route1 = await provider.get_train_route(train1_number)
        route2 = await provider.get_train_route(train2_number)

        if not route1 or not route2:
            return []

        # Find intersection
        stops2_by_code = {s.station_code: s for s in route2}
        common: List[CommonStationOption] = []

        for s1 in route1:
            if s1.station_code in stops2_by_code:
                s2 = stops2_by_code[s1.station_code]
                common.append(
                    CommonStationOption(
                        station_code=s1.station_code,
                        station_name=s1.station_name,
                        train1_sequence=s1.sequence,
                        train2_sequence=s2.sequence,
                        train1_scheduled_arrival=s1.scheduled_arrival or s1.scheduled_departure,
                        train2_scheduled_arrival=s2.scheduled_arrival or s2.scheduled_departure
                    )
                )

        return common

    @classmethod
    async def validate_race_prerequisites(
        cls,
        train1_number: str,
        train2_number: str,
        dest_station_code: str
    ) -> Tuple[bool, str]:
        provider = get_railway_provider()
        t1 = await provider.get_train_details(train1_number)
        if not t1:
            return False, f"Train {train1_number} not found."
        
        t2 = await provider.get_train_details(train2_number)
        if not t2:
            return False, f"Train {train2_number} not found."

        common = await cls.find_common_stations(train1_number, train2_number)
        common_codes = [c.station_code for c in common]

        if dest_station_code.upper() not in common_codes:
            return False, f"Station {dest_station_code} is not a valid common destination for both Train {train1_number} and Train {train2_number}."

        return True, "Valid"

    @classmethod
    async def create_race(
        cls,
        db: AsyncSession,
        train1_number: str,
        train2_number: str,
        dest_station_code: str
    ) -> RaceSession:
        is_valid, err_msg = await cls.validate_race_prerequisites(
            train1_number, train2_number, dest_station_code
        )
        if not is_valid:
            raise ValueError(err_msg)

        provider = get_railway_provider()
        race = RaceSession(
            train1_number=train1_number.strip(),
            train2_number=train2_number.strip(),
            destination_station_code=dest_station_code.strip().upper(),
            status="ACTIVE",
            is_demo=not provider.is_live
        )
        db.add(race)
        await db.commit()
        await db.refresh(race)
        return race

    @classmethod
    async def get_live_race_data(
        cls,
        db: AsyncSession,
        race_id: str
    ) -> LiveRaceComparison:
        # Check cache first to avoid hammering provider
        cache_key = f"race_live_{race_id}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        # Retrieve race from DB
        stmt = select(RaceSession).where(RaceSession.id == race_id)
        result = await db.execute(stmt)
        race = result.scalar_one_or_none()
        if not race:
            raise KeyError(f"Race session {race_id} not found.")

        provider = get_railway_provider()
        
        # Parallel fetch running status for both trains
        status1, status2 = await asyncio.gather(
            provider.get_running_status(race.train1_number, race.destination_station_code),
            provider.get_running_status(race.train2_number, race.destination_station_code)
        )

        # Retrieve recent snapshots
        snap_stmt = select(PredictionSnapshot).where(
            PredictionSnapshot.race_id == race_id
        ).order_by(desc(PredictionSnapshot.timestamp)).limit(20)
        snap_res = await db.execute(snap_stmt)
        db_snapshots = snap_res.scalars().all()

        history_items = [
            PredictionSnapshotItem(
                timestamp=s.timestamp.strftime("%H:%M:%S"),
                train1_delay_min=s.train1_delay_min,
                train2_delay_min=s.train2_delay_min,
                train1_eta=s.train1_eta or "",
                train2_eta=s.train2_eta or "",
                leader_train_number=s.leader_train_number,
                eta_gap_minutes=s.eta_gap_minutes,
                confidence_score=s.confidence_score
            )
            for s in reversed(db_snapshots)
        ]

        # Retrieve lead changes
        lead_stmt = select(LeadChange).where(
            LeadChange.race_id == race_id
        ).order_by(desc(LeadChange.timestamp)).limit(10)
        lead_res = await db.execute(lead_stmt)
        db_leads = lead_res.scalars().all()

        lead_items = [
            LeadChangeItem(
                timestamp=l.timestamp.strftime("%H:%M:%S"),
                previous_leader=l.previous_leader,
                new_leader=l.new_leader,
                margin_minutes=l.margin_minutes,
                reason=l.reason or "Speed / delay variation"
            )
            for l in db_leads
        ]

        prev_snap = history_items[-1] if history_items else None

        # Execute comparison engine
        comparison = TrainComparisonEngine.compare_races(
            race_id=race.id,
            dest_station_code=race.destination_station_code,
            status1=status1,
            status2=status2,
            previous_snapshot=prev_snap,
            history=history_items,
            lead_changes=lead_items,
            next_refresh_sec=30,
            provider_health_status="HEALTHY"
        )

        # Save new snapshot
        new_snap = PredictionSnapshot(
            race_id=race.id,
            timestamp=datetime.now(timezone.utc),
            train1_current_station=comparison.train1.current_station_code,
            train1_delay_min=comparison.train1.current_delay_min,
            train1_eta=comparison.train1.final_predicted_dest_eta,
            train1_speed_kmh=comparison.train1.current_speed_kmh,
            train1_dist_remaining_km=comparison.train1.remaining_distance_km,
            train2_current_station=comparison.train2.current_station_code,
            train2_delay_min=comparison.train2.current_delay_min,
            train2_eta=comparison.train2.final_predicted_dest_eta,
            train2_speed_kmh=comparison.train2.current_speed_kmh,
            train2_dist_remaining_km=comparison.train2.remaining_distance_km,
            leader_train_number=comparison.leader.leader_train_number,
            eta_gap_minutes=comparison.eta_gap_minutes,
            confidence_score=comparison.train1.confidence_score,
            status_level=comparison.train1.level
        )
        db.add(new_snap)

        # Check for lead change
        if prev_snap and prev_snap.leader_train_number != comparison.leader.leader_train_number and not comparison.leader.is_tie:
            lc = LeadChange(
                race_id=race.id,
                timestamp=datetime.now(timezone.utc),
                previous_leader=prev_snap.leader_train_number,
                new_leader=comparison.leader.leader_train_number,
                margin_minutes=comparison.eta_gap_minutes,
                reason=f"Train {comparison.leader.leader_train_number} gained lead with {comparison.eta_gap_minutes}m advantage"
            )
            db.add(lc)
            lead_items.insert(0, LeadChangeItem(
                timestamp=datetime.utcnow().strftime("%H:%M:%S"),
                previous_leader=prev_snap.leader_train_number,
                new_leader=comparison.leader.leader_train_number,
                margin_minutes=comparison.eta_gap_minutes,
                reason=lc.reason
            ))
            comparison.recent_lead_changes = lead_items

        await db.commit()

        # Update cache (15 seconds TTL)
        cache.set(cache_key, comparison, ttl=15)
        return comparison
