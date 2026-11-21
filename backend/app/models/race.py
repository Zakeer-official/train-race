from app.database import Base
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

def generate_race_id():
    return uuid.uuid4().hex[:12]

class RaceSession(Base):
    __tablename__ = "race_sessions"
    
    id = Column(String(32), primary_key=True, default=generate_race_id, index=True)
    train1_number = Column(String(10), nullable=False, index=True)
    train2_number = Column(String(10), nullable=False, index=True)
    destination_station_code = Column(String(10), nullable=False, index=True)
    status = Column(String(20), default="ACTIVE", index=True) # ACTIVE, FINISHED, CANCELLED
    is_demo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    snapshots = relationship("PredictionSnapshot", back_populates="race", cascade="all, delete-orphan", order_by="PredictionSnapshot.timestamp.desc()")
    lead_changes = relationship("LeadChange", back_populates="race", cascade="all, delete-orphan", order_by="LeadChange.timestamp.desc()")

class PredictionSnapshot(Base):
    __tablename__ = "prediction_snapshots"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    race_id = Column(String(32), ForeignKey("race_sessions.id"), index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Train 1 metrics
    train1_current_station = Column(String(20), nullable=True)
    train1_delay_min = Column(Integer, default=0)
    train1_eta = Column(String(30), nullable=True)
    train1_speed_kmh = Column(Float, default=0.0)
    train1_dist_remaining_km = Column(Float, default=0.0)
    
    # Train 2 metrics
    train2_current_station = Column(String(20), nullable=True)
    train2_delay_min = Column(Integer, default=0)
    train2_eta = Column(String(30), nullable=True)
    train2_speed_kmh = Column(Float, default=0.0)
    train2_dist_remaining_km = Column(Float, default=0.0)
    
    # Race comparison
    leader_train_number = Column(String(10), nullable=False)
    eta_gap_minutes = Column(Integer, default=0)
    confidence_score = Column(Float, default=0.90) # 0.0 - 1.0
    status_level = Column(String(20), default="LEVEL_1") # LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4
    
    race = relationship("RaceSession", back_populates="snapshots")

class LeadChange(Base):
    __tablename__ = "lead_changes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    race_id = Column(String(32), ForeignKey("race_sessions.id"), index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    previous_leader = Column(String(10), nullable=False)
    new_leader = Column(String(10), nullable=False)
    margin_minutes = Column(Integer, default=0)
    reason = Column(String(255), nullable=True)
    
    race = relationship("RaceSession", back_populates="lead_changes")
