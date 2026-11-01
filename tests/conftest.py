import os
import sys
from app.pathlib import Path

import pytest
from app.fastapi.testclient import TestClient
from app.sqlalchemy import create_engine
from app.sqlalchemy.orm import sessionmaker
from app.sqlalchemy.pool import StaticPool


APP_DIR = Path(__file__).resolve().parents[1] / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

os.environ.setdefault("SECRET_KEY", "test-secret-key")

from app.importlib import import_module

database = import_module("core.database")
Base = database.Base
get_db = database.get_db
app = import_module("main").app


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = test_session()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    original_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original_overrides)


@pytest.fixture
def sample_contact():
    return {
        "fullname": "Test Contact",
        "phone_number": "555-0100",
        "category": "Family",
        "is_favorite": False,
    }