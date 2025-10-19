from sqlalchemy import Column, String, Integer, DateTime, Text, Numeric, UUID
from sqlalchemy.sql import func
import uuid
from .base import Base

class Investment(Base):
    __tablename__ = "investments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(20), nullable=False)  # 'money', 'time', 'energy'
    category = Column(String(50), nullable=False)  # 'learning', 'job_hunt', 'health'
    title = Column(String(200), nullable=False)
    description = Column(Text)
    amount_invested = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default='hours')  # 'USD', 'EUR', or 'hours' for time
    invested_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Investment(id={self.id}, title='{self.title}', type='{self.type}')>"
