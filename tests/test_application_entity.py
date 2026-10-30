import pytest

from application_entity import ApplicationRecord


def test_initial_state():
    record = ApplicationRecord(1, "Макс")

    assert record.id == 1
    assert record.customer_name == "Макс"
    assert record.status == "new"
    assert record.history == []


def test_change_status():
    record = ApplicationRecord(1, "Макс")
    record.change_status("processing")

    assert record.status == "processing"
    assert record.history == ["processing"]


def test_change_status_2():
    record = ApplicationRecord(1, "Макс")
    record.change_status("processing")
    record.change_status("done")

    assert record.status == "done"
    assert record.history == ["processing", "done"]


def test_repeat_status():
    record = ApplicationRecord(1, "Макс")
    record.change_status("processing")
    record.change_status("processing")

    assert record.status == "processing"
    assert record.history == ["processing"]


def test_unknown_status():
    record = ApplicationRecord(1, "Макс")
    record.change_status("processing")

    with pytest.raises(ValueError, match="Неизвестный статус"):
        record.change_status("unknown")
    assert record.status == "processing"
    assert record.history == ["processing"]


def test_two_objects():
    record = ApplicationRecord(1, "Макс")
    second = ApplicationRecord(10, "second")
    record.change_status("processing")

    assert record.status == "processing"
    assert second.status == "new"
    assert second.history == []
    assert record.history is not second.history
