from model import Application
import pytest


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Оставить заявку" in response.text


def test_get_cat(client):
    response = client.get("/cat", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "https://cataas.com/cat"


def test_create_application(client):
    payload = {"customer_name": "   Max ", "phone": "123", "order_details": "test text for testing"}
    response = client.post("/applications", json=payload)
    created_application = response.json()

    assert response.status_code == 201
    assert type(created_application['id']) is int
    assert created_application['id'] > 0
    assert created_application['customer_name'] == 'Max'
    assert created_application['phone'] == '123'
    assert created_application['order_details'] == 'test text for testing'


def test_get_applications(client):
    payload = {"customer_name": "   Max ", "phone": "123", "order_details": "test text for testing"}
    created_response = client.post("/applications", json=payload)

    assert created_response.status_code == 201

    created_application = created_response.json()
    application_id = created_application['id']
    response = client.get(f"/applications/{application_id}")

    assert response.status_code == 200
    assert response.json() == {"id": application_id, "customer_name": "Max", "phone": "123",
                               "order_details": "test text for testing", "status": "new"}


def test_get_applications_not_found(client):
    response = client.get("/applications/111111111")

    assert response.status_code == 404
    assert response.json() == {"detail": "Заявка не найдена"}


def test_create_application_space_name(client):
    payload = {"customer_name": "   ", "phone": "123", "order_details": "test text for testing"}
    response = client.post("/applications", json=payload)

    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ['body', 'customer_name']


def test_create_application_no_name(client):
    payload = {"phone": "123", "order_details": "test text for testing"}
    response = client.post("/applications", json=payload)

    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ['body', 'customer_name']
    assert response.json()['detail'][0]['type'] == 'missing'


def test_create_application_incorrect_email(client):
    payload = {"customer_name": "Max", "phone": "123", "email": "blabla", "order_details": "test text for testing"}
    response = client.post("/applications", json=payload)

    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ['body', 'email']


def test_create_application_gt_max_length(client):
    payload = {"customer_name": "M" * 21, "phone": "123", "order_details": "test text for testing"}
    response = client.post("/applications", json=payload)

    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ['body', 'customer_name']
    assert response.json()['detail'][0]['type'] == 'string_too_long'


def test_list_applications_empty(client):
    response = client.get("/applications")
    assert response.status_code == 200
    assert response.json() == []


def test_list_applications_no_match(client):
    payload = {"customer_name": "Max", "phone": "123", "email": "blabla@gmail.com",
               "order_details": "test text for testing"}
    create_response = client.post("/applications", json=payload)

    assert create_response.status_code == 201

    response = client.get("/applications?status=done")
    assert response.status_code == 200
    assert response.json() == []


def test_list_applications_default_order(client):
    payload_1 = {"customer_name": "Max", "phone": "123", "email": "blabla@gmail.com",
                 "order_details": "test text for testing"}
    payload_2 = {"customer_name": "Mosk", "phone": "789414", "email": "aaa@gmail.com",
                 "order_details": "new mac"}
    payload_3 = {"customer_name": "user", "phone": "456", "email": "npc@gmail.com",
                 "order_details": "aoaoaoa"}
    create_response_1 = client.post("/applications", json=payload_1)
    create_response_2 = client.post("/applications", json=payload_2)
    create_response_3 = client.post("/applications", json=payload_3)
    response = client.get("/applications")

    assert response.status_code == 200

    post_ids = [create_response_1.json()['id'], create_response_2.json()['id'], create_response_3.json()['id']]
    get_ids = [item["id"] for item in response.json()]

    assert post_ids == get_ids


def test_applications_desc_order(client):
    payload_1 = {"customer_name": "Max", "phone": "123", "email": "blabla@gmail.com",
                 "order_details": "test text for testing"}
    payload_2 = {"customer_name": "Mosk", "phone": "789414", "email": "aaa@gmail.com",
                 "order_details": "new mac"}
    payload_3 = {"customer_name": "user", "phone": "456", "email": "npc@gmail.com",
                 "order_details": "aoaoaoa"}
    create_response_1 = client.post("/applications", json=payload_1)
    create_response_2 = client.post("/applications", json=payload_2)
    create_response_3 = client.post("/applications", json=payload_3)
    response = client.get("/applications?order=desc")

    assert response.status_code == 200

    post_ids = [create_response_3.json()['id'], create_response_2.json()['id'], create_response_1.json()['id']]
    get_ids = [item["id"] for item in response.json()]

    assert post_ids == get_ids


def test_applications_limit(client):
    payload_1 = {"customer_name": "Max", "phone": "123", "email": "blabla@gmail.com",
                 "order_details": "test text for testing"}
    payload_2 = {"customer_name": "Mosk", "phone": "789414", "email": "aaa@gmail.com",
                 "order_details": "new mac"}
    payload_3 = {"customer_name": "user", "phone": "456", "email": "npc@gmail.com",
                 "order_details": "aoaoaoa"}
    create_response_1 = client.post("/applications", json=payload_1)
    create_response_2 = client.post("/applications", json=payload_2)
    create_response_3 = client.post("/applications", json=payload_3)
    response = client.get("/applications?limit=2")

    assert response.status_code == 200

    post_ids = [create_response_1.json()['id'], create_response_2.json()['id']]
    get_ids = [item["id"] for item in response.json()]

    assert get_ids == post_ids


def test_applications_filter_status(client, db_session):
    payload_1 = {"customer_name": "Max", "phone": "123", "email": "blabla@gmail.com",
                 "order_details": "test text for testing"}
    payload_2 = {"customer_name": "Mosk", "phone": "789414", "email": "aaa@gmail.com",
                 "order_details": "new mac"}
    payload_3 = {"customer_name": "user", "phone": "456", "email": "npc@gmail.com",
                 "order_details": "aoaoaoa"}
    create_response_1 = client.post("/applications", json=payload_1)
    create_response_2 = client.post("/applications", json=payload_2)
    create_response_3 = client.post("/applications", json=payload_3)
    second_id = create_response_2.json()["id"]
    second_application = db_session.get(Application, second_id)
    second_application.status = "done"
    db_session.flush()
    response = client.get("/applications?status=new")

    assert response.status_code == 200

    post_ids = [create_response_1.json()['id'], create_response_3.json()['id']]
    get_ids = [item["id"] for item in response.json()]

    assert get_ids == post_ids


def test_applications_params(client, db_session):
    payload_1 = {"customer_name": "Max", "phone": "123", "email": "blabla@gmail.com",
                 "order_details": "test text for testing"}
    payload_2 = {"customer_name": "Mosk", "phone": "789414", "email": "aaa@gmail.com",
                 "order_details": "new mac"}
    payload_3 = {"customer_name": "user", "phone": "456", "email": "npc@gmail.com",
                 "order_details": "aoaoaoa"}
    create_response_1 = client.post("/applications", json=payload_1)
    create_response_2 = client.post("/applications", json=payload_2)
    create_response_3 = client.post("/applications", json=payload_3)
    second_id = create_response_2.json()["id"]
    second_application = db_session.get(Application, second_id)
    second_application.status = "done"
    db_session.flush()
    response = client.get("/applications", params={"status": "new", "order": "desc", "limit": 1})

    assert response.status_code == 200

    post_ids = [create_response_3.json()['id']]
    get_ids = [item["id"] for item in response.json()]

    assert get_ids == post_ids


@pytest.mark.parametrize("limit", [1, 100])
def test_applications_check_limits(client, limit: int):
    payload_1 = {"customer_name": "Max", "phone": "123", "email": "blabla@gmail.com",
                 "order_details": "test text for testing"}
    payload_2 = {"customer_name": "Mosk", "phone": "789414", "email": "aaa@gmail.com",
                 "order_details": "new mac"}
    payload_3 = {"customer_name": "user", "phone": "456", "email": "npc@gmail.com",
                 "order_details": "aoaoaoa"}
    create_response_1 = client.post("/applications", json=payload_1)
    create_response_2 = client.post("/applications", json=payload_2)
    create_response_3 = client.post("/applications", json=payload_3)
    response = client.get("/applications", params={"limit": limit})

    assert response.status_code == 200

    post_ids = [create_response_1.json()['id'], create_response_2.json()['id'], create_response_3.json()['id']]
    get_ids = [item["id"] for item in response.json()]

    assert get_ids == post_ids[:limit]


def test_application_default_limit(client, db_session):
    payload = {"customer_name": "Max", "phone": "123", "email": "blabla@gmail.com",
               "order_details": "test text for testing"}
    create_id = []
    for number in range(21):
        create_response = client.post("/applications", json=payload)
        create_id.append(create_response.json()["id"])
    response = client.get("/applications")

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == create_id[:20]


@pytest.mark.parametrize("params, field", [
    ({"limit": 0}, "limit"), ({"limit": 101}, "limit"), ({"limit": "abc"}, "limit"), (
            {"status": "random"}, "status"), ({"order": "random"}, "order")])
def test_application_error_params(client, params, field):
    response = client.get("/applications", params=params)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", field]


def test_application_filter_status_no_change(client, db_session):
    payload_1 = {"customer_name": "Max", "phone": "123", "email": "blabla@gmail.com",
                 "order_details": "test text for testing"}
    payload_2 = {"customer_name": "Mosk", "phone": "789414", "email": "aaa@gmail.com",
                 "order_details": "new mac"}
    payload_3 = {"customer_name": "user", "phone": "456", "email": "npc@gmail.com",
                 "order_details": "aoaoaoa"}
    create_response_1 = client.post("/applications", json=payload_1)
    create_response_2 = client.post("/applications", json=payload_2)
    create_response_3 = client.post("/applications", json=payload_3)
    second_id = create_response_2.json()["id"]
    second_application = db_session.get(Application, second_id)
    second_application.status = "done"
    db_session.flush()
    response = client.get("/applications", params={"status": "new"})

    assert response.status_code == 200

    post_ids = [create_response_1.json()['id'], create_response_3.json()['id']]
    get_ids = [item["id"] for item in response.json()]

    assert get_ids == post_ids

    new_response = client.get("/applications")

    assert new_response.status_code == 200

    post_new_ids = [create_response_1.json()["id"], create_response_2.json()["id"], create_response_3.json()["id"]]
    get_new_ids = [item["id"] for item in new_response.json()]

    assert get_new_ids == post_new_ids


def test_application_filter_limit_no_change(client, application_payload):
    create_response_1 = client.post("/applications", json=application_payload)
    create_response_2 = client.post("/applications", json=application_payload)
    create_response_3 = client.post("/applications", json=application_payload)
    response = client.get("/applications", params={"limit": 2})

    assert response.status_code == 200

    post_ids = [create_response_1.json()['id'], create_response_2.json()['id']]
    get_ids = [item["id"] for item in response.json()]

    assert get_ids == post_ids

    new_response = client.get("/applications")

    assert new_response.status_code == 200

    post_new_ids = [create_response_1.json()["id"], create_response_2.json()["id"], create_response_3.json()["id"]]
    get_new_ids = [item["id"] for item in new_response.json()]

    assert get_new_ids == post_new_ids


def test_patch_status_new(client, application_status):
    application = application_status(status="new")
    response = client.patch(f"/applications/{application.id}/status", json={"status": "processing"})

    assert response.status_code == 200
    assert response.json()["status"] == "processing"
    assert response.json()["id"] == application.id

    get_response = client.get(f"/applications/{application.id}")

    assert get_response.status_code == 200
    assert get_response.json()["status"] == "processing"


def test_patch_status_processing(client, application_status):
    application = application_status(status="processing")
    response = client.patch(f"/applications/{application.id}/status", json={"status": "done"})

    assert response.status_code == 200
    assert response.json()["status"] == "done"
    assert response.json()["id"] == application.id

    get_response = client.get(f"/applications/{application.id}")

    assert get_response.status_code == 200
    assert get_response.json()["status"] == "done"


def test_patch_status_repeat(client, application_status):
    application = application_status(status="processing")
    response = client.patch(f"/applications/{application.id}/status", json={"status": "processing"})

    assert response.status_code == 200
    assert response.json()["status"] == "processing"
    assert response.json()["id"] == application.id

    get_response = client.get(f"/applications/{application.id}")

    assert get_response.status_code == 200
    assert get_response.json()["status"] == "processing"


@pytest.mark.parametrize('status, new_status', [
    ("new", "done"),
    ("processing", "new"),
    ("done", "new"),
    ("done", "processing"),
])
def test_patch_status_error(client, application_status, status, new_status):
    application = application_status(status=status)
    response = client.patch(f"/applications/{application.id}/status", json={'status': new_status})

    assert response.status_code == 409
    assert response.json()['detail'] == 'Недопустимая смена статуса'

    get_response = client.get(f"/applications/{application.id}")

    assert get_response.status_code == 200
    assert get_response.json()["status"] == status


def test_patch_status_no_application(client, application_status):
    response = client.patch(f"/applications/{1}/status", json={"status": "new"})

    assert response.status_code == 404
    assert response.json()['detail'] == 'Заявка не найдена'


def test_patch_status_random(client, application_status):
    application = application_status(status="new")
    response = client.patch(f"/applications/{application.id}/status", json={"status": "banana"})

    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ['body', 'status']


def test_patch_no_status(client, application_status):
    application = application_status(status="new")
    response = client.patch(f"/applications/{application.id}/status", json={})

    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'missing'


def test_patch_status_none(client, application_status):
    application = application_status(status="new")
    response = client.patch(f"/applications/{application.id}/status", json={'status': None})

    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ['body', 'status']


def test_patch_status_more_than_one(client, application_status):
    application = application_status(status="new")
    response = client.patch(f"/applications/{application.id}/status",
                            json={'status': 'processing', 'customer_name': 'Max'})

    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'extra_forbidden'


@pytest.mark.parametrize('id', [0, -1, 'abc'])
def test_patch_status_incorrect_id(client, application_status, id):
    response = client.patch(f"/applications/{id}/status", json={'status': 'processing'})

    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ['path', 'application_id']
