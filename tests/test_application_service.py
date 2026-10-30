import pytest

from application_service import group_applications_by_status, filter_applications_by_customer
from copy import deepcopy


def test_group_applications_no_change_input():
    applications = [
        {"id": 1, "customer_name": "Макс", "status": "new"},
        {"id": 2, "customer_name": "Анна", "status": "done"},
        {"id": 3, "customer_name": "Борис", "status": "new"},
    ]
    original = deepcopy(applications)
    group_applications_by_status(applications)

    assert applications == original


def test_filter_applications_by_customer_caps():
    applications = [
        {"id": 1, "customer_name": "Макс", "status": "new"},
        {"id": 2, "customer_name": "Анна", "status": "done"},
        {"id": 3, "customer_name": "МАКС", "status": "new"},
    ]
    customer_name = "МАКС"
    result = filter_applications_by_customer(applications, customer_name)

    assert result == [{"id": 1, "customer_name": "Макс", "status": "new"}, {"id": 3, "customer_name": "МАКС", "status": "new"}]


@pytest.mark.parametrize("customer_name", ["", "    "])
def test_filter_applications_by_customer_empty_name(customer_name):
    applications = [
        {"id": 1, "customer_name": "Макс", "status": "new"},
        {"id": 2, "customer_name": "Анна", "status": "done"},
        {"id": 3, "customer_name": "МАКС", "status": "new"},
    ]

    with pytest.raises(ValueError, match="Имя не должно быть пустым"):
        filter_applications_by_customer(applications, "   ")


def test_filter_applications_by_customer_spaces():
    applications = [
        {"id": 1, "customer_name": "Макс", "status": "new"},
        {"id": 2, "customer_name": "Анна", "status": "done"},
        {"id": 3, "customer_name": "МАКС", "status": "new"},
    ]
    customer_name = " МАКС "
    result = filter_applications_by_customer(applications, customer_name)

    assert result == [{"id": 1, "customer_name": "Макс", "status": "new"},
                      {"id": 3, "customer_name": "МАКС", "status": "new"}]


def test_filter_applications_by_customer_full_name():
    applications = [
        {"id": 1, "customer_name": "Максим", "status": "new"},
        {"id": 2, "customer_name": "Анна", "status": "done"},
        {"id": 3, "customer_name": "МАКС", "status": "new"},
    ]
    customer_name = "МАКС"
    result = filter_applications_by_customer(applications, customer_name)

    assert result == [{"id": 3, "customer_name": "МАКС", "status": "new"}]


def test_filter_applications_by_customer_no_customer():
    applications = [
        {"id": 1, "customer_name": "Макс", "status": "new"},
        {"id": 2, "customer_name": "Анна", "status": "done"},
        {"id": 3, "customer_name": "МАКС", "status": "new"},
    ]
    customer_name = "Москвин"
    result = filter_applications_by_customer(applications, customer_name)

    assert result == []


def test_filter_applications_by_customer_empty_list():
    applications = []
    customer_name = "Макс"
    result = filter_applications_by_customer(applications, customer_name)

    assert result == []


def test_filter_applications_by_customer_no_change_input():
    applications = [
        {"id": 1, "customer_name": "Макс", "status": "new"},
        {"id": 2, "customer_name": "Анна", "status": "done"},
        {"id": 3, "customer_name": "МАКС", "status": "new"},
    ]
    original = deepcopy(applications)
    filter_applications_by_customer(applications, "Макс")

    assert applications == original
