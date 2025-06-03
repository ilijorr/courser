import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rel_db import postgres
from models import get_all_models
from main import app

TEST_DB_NAME = "Courser_test"
TEST_USER = "admin"
TEST_PASSWORD = "admin"
TEST_HOST = "localhost"
TEST_PORT = "5432"

test_url = (
        f"postgresql+psycopg2://{TEST_USER}:{TEST_PASSWORD}@"
        f"{TEST_HOST}:{TEST_PORT}/{TEST_DB_NAME}"
        )

@pytest.fixture(name="rel_session")
def rel_session_fixture():
    engine = create_engine(
            test_url,
            echo=True,
            pool_size=10,
            max_overflow=5
            )
    _ = get_all_models()
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(rel_session: Session):
    def get_session_override():
        return rel_session
    
    app.dependency_overrides[postgres.get_db] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()
