from pytest import fixture

from fastapi.testclient import TestClient
from inventory_app.database import Base
from inventory_app.main import app
from inventory_app.routers.items import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


@fixture(scope='module')
def test_app():
    # use an in-memory database
    SQLALCHEMY_DATABASE_URL = "sqlite://"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return app


@fixture(scope='module')
def client(test_app):
    client = TestClient(app)
    return client
