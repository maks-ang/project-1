import json

from application_reader import load_applications
from application_service import find_application_by_id, filter_applications_by_status, group_applications_by_status, filter_applications_by_customer


def main():
    try:
        requested_id = int(input("Введите ID заявки: "))
    except ValueError:
        return "ID должен быть целым числом"
    try:
        applications = load_applications("applications.json")
    except FileNotFoundError:
        return "Файл не найден"
    except json.JSONDecodeError:
        return "Файл повреждён"
    except ValueError as error:
        return f"Неправильная структура заявок: {error}"
    else:
        find_id = find_application_by_id(applications, requested_id)
        filter_status = filter_applications_by_status(applications, "new")
        group = group_applications_by_status(applications)
        if find_id is None:
            find_result = f"Заявка с id {requested_id} не найдена"
        else:
            find_result = f"Найдена заявка {find_id["id"]}: {find_id["customer_name"]}"
        group_list = []
        for status, items in group.items():
            group_list.append(f"{status}: {len(items)}")
        group_text = "\n".join(group_list)
        name = input("Введите имя: ")
        try:
            customer_applications = filter_applications_by_customer(applications, name)
        except ValueError as error:
            customer_result = f"Ошибка поиска по имени: {error}"
        else:
            if customer_applications:
                customer_result = (
                    f"Заявок клиента «{name.strip()}»: "
                    f"{len(customer_applications)}"
                )
            else:
                customer_result = "Заявки этого клиента не найдены"
        return f'''Всего заявок: {len(applications)}
{find_result}
Новых заявок: {len(filter_status)}
{group_text}
{customer_result}'''


if __name__ == "__main__":
    print(main())
