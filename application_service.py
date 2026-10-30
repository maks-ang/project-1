applications = [
    {"id": 1, "customer_name": "Макс", "status": "new"},
    {"id": 2, "customer_name": "Анна", "status": "done"},
    {"id": 3, "customer_name": "МАКС", "status": "new"},
]


def find_application_by_id(applications, application_id):
    for application in applications:
        if application["id"] == application_id:
            return application
    return None


def filter_applications_by_status(applications, status):
    application_list =[]
    for application in applications:
        if application["status"] == status:
            application_list.append(application)
    return application_list


def group_applications_by_status(applications):
    group_dict = {}
    for application in applications:
        group_dict.setdefault(application["status"], []).append(application)
    return group_dict


def filter_applications_by_customer(applications, customer_name):
    customer_list = []
    check_name = customer_name.strip().lower()
    if not check_name:
        raise ValueError("Имя не должно быть пустым")
    for application in applications:
        if application["customer_name"].lower().strip() == check_name:
            customer_list.append(application)
    return customer_list
