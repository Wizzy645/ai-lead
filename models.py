from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from database import Base


class SalesLead(Base):
    """Table to store structured data extracted by the AI from sales inquiries."""
    __tablename__ = "sales_leads"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    company_name = Column(String, nullable=True)
    budget = Column(String, nullable=True)
    original_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
