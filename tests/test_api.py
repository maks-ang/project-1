from fastapi.testclient import TestClient

from main import app
from schemas import ApplicationCreate


def test_home():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")
        assert "Оставить заявку" in response.text


def test_get_cat():
    with TestClient(app) as client:
        response = client.get("/cat", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "https://cataas.com/cat"


def test_create_application():
    with TestClient(app) as client:
        labels = {"customer_name": "Max", "phone": "123", "order_details": "test text for testing"}
        response = client.post("/applications", data=labels, follow_redirects=False)
        assert response.status_code == 303
        assert response.headers["location"] == "/"


def test_get_applications():
    with TestClient(app) as client:
        response = client.get("/applications/10", follow_redirects=False)
        assert response.status_code == 200
        assert response.json() == {"id": 10, "customer_name": "Max", "phone": "123", "order_details": "test text for testing"}


def test_get_applications_not_found():
    with TestClient(app) as client:
        response = client.get("/applications/111111111", follow_redirects=False)
        assert response.status_code == 404
        assert response.json() == {"detail": "Заявка не найдена"}


def test_create_application_space_name():
    with TestClient(app) as client:
        labels = {"customer_name": "   ", "phone": "123", "order_details": "test text for testing"}
        response = client.post("/applications", data=labels, follow_redirects=False)

        assert response.status_code == 422
        assert response.json()['detail'][0]['loc'] == ['body', 'customer_name']


def test_create_application_no_name():
    with TestClient(app) as client:
        labels = {"phone": "123", "order_details": "test text for testing"}
        response = client.post("/applications", data=labels, follow_redirects=False)

        assert response.status_code == 422
        assert response.json()['detail'][0]['loc'] == ['body', 'customer_name']
        assert response.json()['detail'][0]['type'] == 'missing'


def test_create_application_incorrect_email():
    with TestClient(app) as client:
        labels = {"customer_name": "Max", "phone": "123", "email": "blabla" ,"order_details": "test text for testing"}
        response = client.post("/applications", data=labels, follow_redirects=False)

        assert response.status_code == 422
        assert response.json()['detail'][0]['loc'] == ['body', 'email']


def test_create_application_gt_max_length():
    with TestClient(app) as client:
        labels = {"customer_name": "M" * 21, "phone": "123", "order_details": "test text for testing"}
        response = client.post("/applications", data=labels, follow_redirects=False)

        assert response.status_code == 422
        assert response.json()['detail'][0]['loc'] == ['body', 'customer_name']
        assert response.json()['detail'][0]['type'] == 'string_too_long'


def test_create_application_strip_name():
        labels = {"customer_name": "    Max   ", "phone": "123", "order_details": "test text for testing"}
        application = ApplicationCreate(**labels)
        assert application.customer_name == "Max"

