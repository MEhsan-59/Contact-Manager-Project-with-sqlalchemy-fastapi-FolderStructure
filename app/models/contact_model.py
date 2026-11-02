from sqlalchemy import Boolean, Column, Integer, String, BigInteger
from sqlalchemy.orm import validates
from app.core.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100), nullable=False, index=True, unique=True)
    phone_number = Column(String(20), nullable=False, index=True)
    is_favorite = Column(Boolean, default=False, nullable=False)
    category = Column(String(20), nullable=False, index=True)
    
    @validates("fullname")
    def convert_fullname_to_title(self, key, value):
        return value.title()