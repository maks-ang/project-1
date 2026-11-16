import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from database import get_db
from main import app
from model import Application


@pytest.fixture(scope="session")
def test_engine():
    database_url = os.environ["TEST_DATABASE_URL"]

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
def session():
    engine = create_engine('postgresql+psycopg://n0tthesame@localhost:5432/sql_practice')
    with engine.connect() as connection:
        transaction = connection.begin()
        session = Session(bind=connection, join_transaction_mode="create_savepoint")
        try:
            yield session
        finally:
            session.close()
            transaction.rollback()
    engine.dispose()
