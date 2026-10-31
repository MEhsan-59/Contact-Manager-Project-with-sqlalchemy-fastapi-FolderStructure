from core.logger_setup import logger
from core.database import Base, engine
from models.contact import Contact

print("Tables known to Base:", list(Base.metadata.tables.keys()))
Base.metadata.create_all(bind=engine)
print("Done")