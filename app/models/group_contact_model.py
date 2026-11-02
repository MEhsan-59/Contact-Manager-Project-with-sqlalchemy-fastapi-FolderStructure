from sqlalchemy import Column, DateTime, ForeignKey,Integer, UniqueConstraint, func
from app.core.database import Base


class GroupContact(Base):
    __tablename__ = "group_contacts"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.group_id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    added_at = Column(DateTime(timezone=True), server_default=func.now())


    __table_args__ = (
        UniqueConstraint("group_id", "contact_id", name="uq_group_contact"),
    )