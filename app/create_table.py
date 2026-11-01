from app.core.logger_setup import logger
from app.core.database import Base, engine
from app.models.contact import Contact

print("Tables known to Base:", list(Base.metadata.tables.keys()))
Base.metadata.create_all(bind=engine)
print("Done")