from pytest import fixture

from fastapi.testclient import TestClient
from inventory_app.database import Base
from inventory_app.main import app
from inventory_app.models import Item, User
from inventory_app.routers.users import bcrypt_context
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from sqlalchemy.pool import StaticPool

# use an in-memory database so no database file is created
# each test run starts from clear database
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

expected_item = {
    "name": "water gun",
    "description": "no harm",
    "category": "weapon",
    "quantity": 5,
    "price": 100.5,
    # owner id matches with the current user id
    "owner_id": 1,
    "id": 1
}


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "bob", "id": 1, "role": "admin"}


@fixture(scope="module", )
def test_app(request):
    # db and user get from requesting module
    # e.g. admin, items import own get_db and get_current_user functions
    module_name = request.module.__name__.split("_")[-1]
    get_db = getattr(request.module, f"{module_name}_get_db")
    get_current_user = getattr(request.module, f"{module_name}_get_current_user")

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    return app


@fixture(scope="module")
def client(test_app):
    client = TestClient(app)
    return client


@fixture()
def test_item():
    test_item_weapon = {
        "name": "water gun",
        "description": "no harm",
        "category": "weapon",
        "quantity": 5,
        "price": 100.5,
        # owner id matches with the current user id
        "owner_id": 1
    }

    db = TestingSessionLocal()
    db_item = Item(**test_item_weapon)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    yield test_item_weapon
    clear_table("items")


@fixture()
def tear_down_clear_items_table():
    yield
    clear_table("items")


@fixture()
def test_user():
    user = {
        "username": "bob",
        "email": "bob@gmail.com",
        "first_name": "bob",
        "last_name": "smith",
        "hashed_password": bcrypt_context.hash("test123"),
        "role": "admin"
    }

    db = TestingSessionLocal()
    db_item = User(**user)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    yield user
    clear_table("users")


def clear_table(table_name):
    with engine.connect() as connection:
        connection.execute(text(f"DELETE FROM {table_name};"))
        connection.commit()


def get_db_item_by_id(item_id: int):
    db = TestingSessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    return db_item
