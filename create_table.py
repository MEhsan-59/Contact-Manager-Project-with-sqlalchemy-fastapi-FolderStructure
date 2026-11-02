from app.core.logger_setup import logger
from app.core.database import Base, engine
from app.models.contact_model import Contact
from app.models.group_model import Group
from app.models.group_contact_model import GroupContact
print("Tables known to Base:", list(Base.metadata.tables.keys()))
Base.metadata.create_all(bind=engine)
print("Done")