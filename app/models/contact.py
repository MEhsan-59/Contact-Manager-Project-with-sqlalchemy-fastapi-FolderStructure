from sqlalchemy import Boolean, Column, Integer, String, BigInteger
from core.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100), nullable=False, index=True)
    phone_number = Column(String(20), nullable=False, index=True)
    favorite = Column(Boolean, default=False, nullable=False)
    category = Column(String(20), nullable=False, index=True)
    