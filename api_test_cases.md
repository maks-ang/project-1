# Сценарии проверки заявок

POST /applications принимает JSON.
Успешное создание возвращает 201 и JSON заявки.
API-тесты используют отдельную базу test_db.
Изменения каждого API-теста откатываются после его завершения.

## API-тесты заявок

| Сценарий | Подготовка и входные данные | Метод и путь | Ожидаемый результат | Тест |
| --- | --- | --- | --- | --- |
| Успешное создание | JSON: имя "   Max ", телефон "123", описание "test text for testing"; email пропущен | POST /applications | 201; id — положительное целое число; customer_name равен "Max"; phone и order_details совпадают с отправленными | test_create_application |
| Найденная заявка | Тест создаёт заявку через POST и получает её ID из ответа | GET /applications/{созданный_id} | 200; JSON равен ожидаемому объекту с полями id, customer_name, phone, order_details | test_get_applications |
| Отсутствующая заявка | Тестовая таблица заявок пуста; ID 111111111 отсутствует | GET /applications/111111111 | 404; JSON равен {"detail": "Заявка не найдена"} | test_get_applications_not_found |
| Имя из пробелов | JSON: customer_name содержит только пробелы; остальные обязательные поля корректны | POST /applications | 422; loc первой ошибки равен ["body", "customer_name"] | test_create_application_space_name |
| Имя пропущено | JSON: ключ customer_name отсутствует; остальные обязательные поля корректны | POST /applications | 422; loc первой ошибки равен ["body", "customer_name"]; type равен "missing" | test_create_application_no_name |
| Неправильный email | JSON: email равен "blabla"; остальные поля корректны | POST /applications | 422; loc первой ошибки равен ["body", "email"] | test_create_application_incorrect_email |
| Слишком длинное имя | JSON: customer_name содержит 21 символ при максимуме 20; остальные поля корректны | POST /applications | 422; loc первой ошибки равен ["body", "customer_name"]; type равен "string_too_long" | test_create_application_gt_max_length |

## Проверка Pydantic-схемы без HTTP

| Сценарий | Входные данные | Ожидаемый результат | Тест |
| --- | --- | --- | --- |
| Удаление пробелов вокруг имени | ApplicationCreate получает customer_name="   Max   "; остальные обязательные поля корректны | У созданного объекта customer_name равен "Max" | test_create_application_strip_name |
## Получение списка заявок

Все тесты используют отдельную базу test_db.
Изменения откатываются после каждого теста.
Ожидаемые ID берутся из созданных записей, а не задаются вручную.

| Сценарий | Подготовка и параметры | Ожидаемый результат | Тест |
| --- | --- | --- | --- |
| Пустая база | Заявки не создаются; GET /applications без параметров | 200 и [] | test_list_applications_empty |
| Нет совпадений | Создана заявка new; status=done | 200 и [] | test_list_applications_no_match |
| Порядок по умолчанию | Созданы три заявки; параметры отсутствуют | 200; все три ID по возрастанию | test_list_applications_default_order |
| Обратный порядок | Созданы три заявки; order=desc | 200; все три ID по убыванию | test_applications_desc_order |
| Ограничение количества | Созданы три заявки; limit=2 | 200; первые два ID по возрастанию | test_applications_limit |
| Фильтр по статусу | Созданы заявки new, done, new; status=new | 200; только ID заявок new по возрастанию | test_applications_filter_status |
| Совместная работа параметров | Созданы заявки разных статусов; status=new, order=desc, limit=2 | 200; два наибольших ID среди заявок new, по убыванию | test_applications_params |
| Минимальный limit | Созданы три заявки; limit=1 | 200; только первая заявка по ID | test_applications_check_limits[1] |
| Максимальный допустимый limit | Созданы три заявки; limit=100 | 200; все три заявки по возрастанию ID | test_applications_check_limits[100] |
| Limit по умолчанию | Создана 21 заявка; limit пропущен | 200; первые 20 ID по возрастанию | test_application_default_limit |
| Limit меньше минимума | limit=0 | 422; loc ошибки равен ["query", "limit"] | test_application_error_params |
| Limit больше максимума | limit=101 | 422; loc ошибки равен ["query", "limit"] | test_application_error_params |
| Нечисловой limit | limit=abc | 422; loc ошибки равен ["query", "limit"] | test_application_error_params |
| Неизвестный статус | status=random | 422; loc ошибки равен ["query", "status"] | test_application_error_params |
| Неизвестный порядок | order=random | 422; loc ошибки равен ["query", "order"] | test_application_error_params |
| Независимость фильтра | Первый запрос с status=new; второй без фильтра | Первый возвращает только new; второй — все подготовленные заявки | test_application_filter_status_no_change |
| Независимость limit | Созданы три заявки; первый запрос с limit=2; второй без limit | Первый возвращает две заявки; второй — все три | test_application_filter_limit_no_change |