| Сценарий | Подготовка и входные данные | Метод и путь | Ожидаемый результат | Тест |
| --- | --- | --- | --- | --- |
| Успешное создание | Имя Max, телефон 123, непустое описание; email пропущен | POST /applications | 303; заголовок Location равен / | test_create_application |
| Найденная заявка | В БД существует заявка 10 с ожидаемыми данными | GET /applications/10 | 200; JSON содержит ожидаемые id, customer_name, phone, order_details | test_get_applications |
| Отсутствующая заявка | В БД нет заявки 111111111 | GET /applications/111111111 | 404; detail равен «Заявка не найдена» | test_get_applications_not_found |
| Имя из пробелов | customer_name содержит только пробелы | POST /applications | 422; loc ошибки равен ["body", "customer_name"] | test_create_application_space_name |
| Имя пропущено | Ключ customer_name отсутствует | POST /applications | 422; ошибка customer_name с типом missing | test_create_application_no_name |
| Неправильный email | email равен blabla | POST /applications | 422; loc ошибки равен ["body", "email"] | test_create_application_incorrect_email |
| Слишком длинное имя | customer_name содержит 21 символ при максимуме 20 | POST /applications | 422; ошибка customer_name с типом string_too_long | test_create_application_gt_max_length |