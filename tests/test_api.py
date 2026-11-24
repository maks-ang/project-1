import pytest
from model import Application


def test_create_application(client, application_payload):
    response = client.post("/applications", json=application_payload | {"customer_name": "   Max "})
    body = response.json()

    assert response.status_code == 201
    assert isinstance(body["id"], int) and body["id"] > 0
    assert body["customer_name"] == "Max"
    assert body["phone"] == "123"
    assert body["order_details"] == "test text for testing"


def test_get_applications(client, create_application):
    response = client.get(f"/applications/{create_application['id']}")

    assert response.status_code == 200
    assert response.json() == {"id": create_application["id"], "customer_name": "Max", "phone": "123",
                               "order_details": "test text for testing", "status": "new"}


@pytest.mark.parametrize("change, loc", [
    ({"customer_name": "   "}, "customer_name"),
    ({"customer_name": "M" * 21}, "customer_name"),
    ({"email": "blabla"}, "email"),
])
def test_create_application_invalid(client, application_payload, change, loc):
    response = client.post("/applications", json=application_payload | change)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", loc]


def test_create_application_no_name(client, application_payload):
    del application_payload["customer_name"]
    response = client.post("/applications", json=application_payload)

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"


def test_create_application_too_long_name(client, application_payload):
    response = client.post("/applications", json=application_payload | {"customer_name": "M" * 21})

    assert response.json()["detail"][0]["type"] == "string_too_long"


def test_list_applications_no_match(client, create_application):
    response = client.get("/applications?status=done")

    assert response.status_code == 200
    assert response.json() == []


def test_list_applications_default_order(client, three_apps):
    ids = [app["id"] for app in three_apps]
    response = client.get("/applications")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == ids


def test_applications_desc_order(client, three_apps):
    ids = [app["id"] for app in three_apps]
    response = client.get("/applications?order=desc")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == ids[::-1]


def test_applications_limit(client, three_apps):
    ids = [app["id"] for app in three_apps]
    response = client.get("/applications?limit=2")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == ids[:2]


def test_applications_filter_status(client, db_session, three_apps):
    db_session.get(Application, three_apps[1]["id"]).status = "done"
    db_session.flush()
    response = client.get("/applications?status=new")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [three_apps[0]["id"], three_apps[2]["id"]]


def test_applications_params(client, db_session, three_apps):
    db_session.get(Application, three_apps[1]["id"]).status = "done"
    db_session.flush()
    response = client.get("/applications", params={"status": "new", "order": "desc", "limit": 1})

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [three_apps[2]["id"]]


@pytest.mark.parametrize("limit", [1, 100])
def test_applications_check_limits(client, three_apps, limit):
    ids = [app["id"] for app in three_apps]
    response = client.get("/applications", params={"limit": limit})

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == ids[:limit]


def test_application_default_limit(client, application_payload):
    ids = [client.post("/applications", json=application_payload).json()["id"] for _ in range(21)]
    response = client.get("/applications")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == ids[:20]


def test_application_filter_status_no_change(client, db_session, three_apps):
    ids = [app["id"] for app in three_apps]
    db_session.get(Application, ids[1]).status = "done"
    db_session.flush()

    response = client.get("/applications", params={"status": "new"})
    assert [item["id"] for item in response.json()] == [ids[0], ids[2]]

    all_response = client.get("/applications")
    assert [item["id"] for item in all_response.json()] == ids


def test_application_filter_limit_no_change(client, three_apps):
    ids = [app["id"] for app in three_apps]

    response = client.get("/applications", params={"limit": 2})
    assert [item["id"] for item in response.json()] == ids[:2]

    all_response = client.get("/applications")
    assert [item["id"] for item in all_response.json()] == ids


@pytest.mark.parametrize("current, new", [
    ("new", "processing"),
    ("processing", "done"),
    ("processing", "processing"),
])
def test_patch_status_ok(client, application_status, current, new):
    application = application_status(status=current)
    response = client.patch(f"/applications/{application.id}/status", json={"status": new})

    assert response.status_code == 200
    assert response.json()["status"] == new
    assert response.json()["id"] == application.id
    assert client.get(f"/applications/{application.id}").json()["status"] == new
