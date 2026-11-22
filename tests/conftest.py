import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from database import get_db
from main import app
from model import Application
from orm_practice.models import User, Event

@pytest.fixture(scope="session")
def test_engine():
    database_url = os.environ.setdefault("TEST_DATABASE_URL", "postgresql+psycopg://n0tthesame@localhost:5432/test_db")

    if make_url(database_url).database != "test_db":
        raise RuntimeError("Тесты должны использовать базу test_db")

    engine = create_engine(database_url)

    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def db_session(test_engine):
    with test_engine.connect() as connection:
        transaction = connection.begin()

        session = Session(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )

        try:
            yield session
        finally:
            session.close()
            transaction.rollback()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    previous_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous_overrides)


@pytest.fixture
def application_payload():
    return {"customer_name": "Max", "phone": "123", "email": "blabla@gmail.com",
            "order_details": "test text for testing"}


@pytest.fixture
def create_application(client, application_payload):
    response = client.post("/applications", json=application_payload)

    assert response.status_code == 201
    return response.json()


@pytest.fixture
def application_status(db_session):
    def create_application(**overrides):
        payload = {"customer_name": "Max", "phone": "123", "email": "blabla@gmail.com",
                   "order_details": "test text for testing"}
        payload.update(overrides)
        application = Application(**payload)
        db_session.add(application)
        db_session.flush()
        return application

    return create_application


@pytest.fixture
def user(db_session):
    user = User(name="Тест", email="test@example.com")
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture
def event(db_session):
    event = Event(title="Тестовое событие", seats_left=2)
    db_session.add(event)
    db_session.flush()
    return event
