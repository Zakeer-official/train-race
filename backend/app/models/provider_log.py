from app.database import Base
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text
from datetime import datetime

class APIHealthLog(Base):
    __tablename__ = "api_health_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    provider_name = Column(String(50), nullable=False, index=True)
    endpoint = Column(String(255), nullable=False)
    status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Float, nullable=False)
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
