from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from models import get_all_models
from core.settings import RelationalSettings, SettingsFactory

db_settings = SettingsFactory.create(RelationalSettings)
engine = create_engine(
        db_settings.url,
        echo=True,
        pool_size=10,
        max_overflow=5
        )

def create_db_and_tables(drop_all: bool = False):
    _ = get_all_models()
    with engine.begin() as conn:
        if drop_all:
            SQLModel.metadata.drop_all(conn)
        SQLModel.metadata.create_all(conn)

SessionLocal = sessionmaker(
        autoflush=False,
        bind=engine
        )

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
