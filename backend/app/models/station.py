from app.database import Base
from sqlalchemy import Column, String, Integer, Float, DateTime
from datetime import datetime

class Station(Base):
    __tablename__ = "stations"
    
    code = Column(String(10), primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    state = Column(String(50), nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
