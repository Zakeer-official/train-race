from app.database import Base
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Train(Base):
    __tablename__ = "trains"
    
    number = Column(String(10), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    train_type = Column(String(50), default="SUPERFAST")
    source_station_code = Column(String(10), nullable=False)
    dest_station_code = Column(String(10), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    stops = relationship("TrainStop", back_populates="train", cascade="all, delete-orphan", order_by="TrainStop.sequence")

class TrainStop(Base):
    __tablename__ = "train_stops"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    train_number = Column(String(10), ForeignKey("trains.number"), index=True, nullable=False)
    station_code = Column(String(10), index=True, nullable=False)
    station_name = Column(String(100), nullable=False)
    sequence = Column(Integer, nullable=False)
    scheduled_arrival = Column(String(10), nullable=True) # e.g. "14:35"
    scheduled_departure = Column(String(10), nullable=True) # e.g. "14:40"
    distance_km = Column(Float, default=0.0)
    day_count = Column(Integer, default=1)
    
    train = relationship("Train", back_populates="stops")
