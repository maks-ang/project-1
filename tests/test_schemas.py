from schemas import CreateSchema


def test_create_application_strip_name():
    payload = {"customer_name": "    Max   ", "phone": "123", "order_details": "test text for testing"}
    application = CreateSchema(**payload)

    assert application.customer_name == "Max"
