import pytest
import json

from application_reader import load_applications, validate_unique_ids

def test_load_applications(tmp_path):
    path = tmp_path / "applications.json"
    path.write_text('[{"id": 1, "customer_name": "Макс", "phone": "000", "order_details": "Учебная заявка", "status": "new"}]')
    result = load_applications(path)
    assert result == [{"id": 1, "customer_name": "Макс", "phone": "000", "order_details": "Учебная заявка", "status": "new"}]


def test_load_applications_missing_file(tmp_path):
    path = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        load_applications(path)


def test_load_applications_broken_file(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text('{"id" :')
    with pytest.raises(json.JSONDecodeError):
        load_applications(path)


def test_validate_applications(tmp_path):
    path = tmp_path / "random.json"
    path.write_text('"bla bla bla"')
    with pytest.raises(ValueError,match="Ожидался список заявок"):
        load_applications(path)


def test_validate_keys(tmp_path):
    path = tmp_path / "something.json"
    path.write_text('[{"id": 1, "customer_name": "Макс", "order_details": "Учебная заявка"}]')
    with pytest.raises(ValueError, match="Отсутствуют обязательные ключи"):
        load_applications(path)


def test_validate_unique_ids():
    data = [{"id": 1}, {"id": 2}]

    validate_unique_ids(data)


def test_validate_unique_ids_repeat():
    data = [{"id": 1}, {"id": 1}]

    with pytest.raises(ValueError, match="ID занят"):
        validate_unique_ids(data)


def test_validate_unique_ids_nothing():
    validate_unique_ids([])

def test_load_applications_rejects_duplicate_ids(tmp_path):
    path = tmp_path / "duplicate_ids.json"
    data = [
        {
            "id": 1,
            "customer_name": "Макс",
            "phone": "123",
            "order_details": "Первая заявка",
            "status": "new",
        },
        {
            "id": 1,
            "customer_name": "Анна",
            "phone": "456",
            "order_details": "Вторая заявка",
            "status": "done",
        },
    ]
    path.write_text(json.dumps(data, ensure_ascii=False))

    with pytest.raises(ValueError, match="ID занят"):
        load_applications(path)
