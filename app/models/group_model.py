from sqlalchemy import BigInteger, Column, DateTime, Integer, String, func
from app.core.database import Base
from sqlalchemy.orm import relationship, validates

class Group(Base):
    __tablename__ = "groups"
    group_id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String, unique=True, nullable=False)
    create_at = Column(DateTime(timezone=True), server_default=func.now())


    @validates("group_name")
    def convert_group_name_to_title(self, key, value):
        return value.title()