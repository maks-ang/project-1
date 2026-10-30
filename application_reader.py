import json

def load_applications(path):
    with open(path) as file:
         data = json.load(file)
    validate_applications(data)
    validate_keys(data)
    validate_unique_ids(data)
    return data


def validate_applications(data):
    if not isinstance(data, list):
        raise ValueError("Ожидался список заявок")


def validate_keys(data):
    validate_key = ("id", "customer_name", "phone", "order_details", "status")
    for application in data:
        for key in validate_key:
            if key not in application:
                raise ValueError("Отсутствуют обязательные ключи")


def validate_unique_ids(data):
    ids = set()
    for application in data:
        application_id = application["id"]
        if application_id in ids:
            raise ValueError("ID занят")
        else:
            ids.add(application_id)