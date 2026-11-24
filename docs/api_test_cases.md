# Сценарии проверки API

## Окружение

API-тесты используют отдельную PostgreSQL-базу test_db.

Адрес задаётся через TEST_DATABASE_URL. Фикстура проверяет имя базы перед подключением.

Зависимость get_db подменяется тестовой сессией. После каждого теста изменения откатываются, подмена зависимости снимается.

Тестовая таблица перед запуском должна быть пустой. Откат теста не удаляет записи, существовавшие до его начала.

ID берутся из созданных записей, а не задаются заранее. После отката последовательность ID может продолжать расти.

## Главная страница и перенаправление

| Сценарий | Запрос | Ожидаемый результат | Тест |
| --- | --- | --- | --- |
| Главная страница | GET / | 200; Content-Type начинается с text/html; страница содержит «Оставить заявку» | test_home |
| Перенаправление на изображение | GET /cat без перехода по редиректу | 307; Location равен https://cataas.com/cat | test_get_cat |

## Создание заявки

POST-запросы отправляют JSON. Если не указано иное, остальные обязательные поля корректны.

| Сценарий | Входные данные | Проверяемый результат | Тест |
| --- | --- | --- | --- |
| Успешное создание и очистка имени | Имя "   Max ", телефон "123", непустое описание; email пропущен | 201; ID — положительное целое число; имя равно "Max"; телефон и описание соответствуют отправленным | test_create_application |
| Имя из пробелов | customer_name содержит только пробелы | 422; loc первой ошибки равен ["body", "customer_name"] | test_create_application_space_name |
| Имя пропущено | Ключ customer_name отсутствует | 422; loc равен ["body", "customer_name"]; type равен missing | test_create_application_no_name |
| Неправильный email | email равен "blabla" | 422; loc равен ["body", "email"] | test_create_application_incorrect_email |
| Слишком длинное имя | Имя содержит 21 символ при максимуме 20 | 422; loc равен ["body", "customer_name"]; type равен string_too_long | test_create_application_gt_max_length |

## Получение одной заявки

| Сценарий | Подготовка и запрос | Проверяемый результат | Тест |
| --- | --- | --- | --- |
| Найденная заявка | Создать заявку через POST; выполнить GET /applications/{полученный_id} | 200; JSON целиком совпадает с ожидаемыми id, customer_name, phone, order_details и status="new" | test_get_applications |
| Отсутствующая заявка | В пустой тестовой таблице запросить GET /applications/111111111 | 404; JSON равен {"detail": "Заявка не найдена"} | test_get_applications_not_found |

## Получение списка заявок

Все запросы выполняются методом GET по пути /applications.

| Сценарий | Подготовка и параметры | Проверяемый результат | Тест |
| --- | --- | --- | --- |
| Пустая база | Не создавать заявки; параметры отсутствуют | 200 и [] | test_list_applications_empty |
| Нет совпадений | Создать заявку new; status=done | 200 и [] | test_list_applications_no_match |
| Порядок по умолчанию | Три заявки; параметры отсутствуют | 200; все три ID по возрастанию | test_list_applications_default_order |
| Обратный порядок | Три заявки; order=desc | 200; все три ID по убыванию | test_applications_desc_order |
| Ограничение количества | Три заявки; limit=2 | 200; первые два ID по возрастанию | test_applications_limit |
| Фильтр по статусу | Заявки new, done, new; status=new | 200; только ID первой и третьей заявок | test_applications_filter_status |
| Совместная работа параметров | Заявки new, done, new; status=new, order=desc, limit=1 | 200; только наибольший ID среди заявок new | test_applications_params |
| Минимальный limit | Три заявки; limit=1 | 200; первая заявка по ID | test_applications_check_limits[1] |
| Максимальный допустимый limit | Три заявки; limit=100 | 200; все три заявки по возрастанию ID | test_applications_check_limits[100] |
| Limit по умолчанию | Создать 21 заявку; limit пропущен | 200; первые 20 ID по возрастанию | test_application_default_limit |
| Limit ниже минимума | limit=0 | 422; loc равен ["query", "limit"] | test_application_error_params |
| Limit выше максимума | limit=101 | 422; loc равен ["query", "limit"] | test_application_error_params |
| Нечисловой limit | limit=abc | 422; loc равен ["query", "limit"] | test_application_error_params |
| Неизвестный статус | status=random | 422; loc равен ["query", "status"] | test_application_error_params |
| Неизвестный порядок | order=random | 422; loc равен ["query", "order"] | test_application_error_params |
| Независимость фильтра | Первый запрос с status=new; второй без фильтра | Первый возвращает только new; второй — все три подготовленные заявки | test_application_filter_status_no_change |
| Независимость limit | Три заявки; первый запрос с limit=2; второй без limit | Первый возвращает первые две заявки; второй — все три | test_application_filter_limit_no_change |

## Изменение статуса

PATCH-запросы выполняются по пути /applications/{id}/status и отправляют JSON.

Начальное состояние готовится ORM-фабрикой application_status.

| Сценарий | Начальное состояние и вход | Проверяемый результат | Тест |
| --- | --- | --- | --- |
| new → processing | Заявка new; {"status": "processing"} | 200; ID сохранён; PATCH и последующий GET показывают processing | test_patch_status_new |
| processing → done | Заявка processing; {"status": "done"} | 200; ID сохранён; PATCH и последующий GET показывают done | test_patch_status_processing |
| Повтор текущего статуса | Заявка processing; {"status": "processing"} | 200; ID сохранён; PATCH и GET показывают processing | test_patch_status_repeat |
| Запрещённые переходы | Пары new → done, processing → new, done → new, done → processing | 409; detail равен «Недопустимая смена статуса»; последующий GET показывает исходный статус | test_patch_status_error |
| Отсутствующая заявка | Пустая таблица; ID 1; {"status": "new"} | 404; detail равен «Заявка не найдена» | test_patch_status_no_application |
| Неизвестный статус | Существующая заявка new; {"status": "banana"} | 422; loc равен ["body", "status"] | test_patch_status_random |
| Статус пропущен | Существующая заявка; {} | 422; type равен missing | test_patch_no_status |
| Статус null | Существующая заявка; {"status": null} | 422; loc равен ["body", "status"] | test_patch_status_none |
| Лишнее поле | Существующая заявка; status и customer_name | 422; type равен extra_forbidden | test_patch_status_more_than_one |
| Некорректный ID | ID 0, -1 или abc; {"status": "processing"} | 422; loc равен ["path", "application_id"] | test_patch_status_incorrect_id |

## Проверка Pydantic-схемы без HTTP

Файл: tests/test_schemas.py.

| Сценарий | Вход | Проверяемый результат | Тест |
| --- | --- | --- | --- |
| Очистка имени | CreateSchema получает имя "    Max   " и корректные обязательные поля | customer_name равен "Max" | test_create_application_strip_name |

## Границы текущего покрытия

- Тест создания проверяет ID, имя, телефон и описание; статус new дополнительно проверяется в сценарии получения созданной заявки.
- Проверка limit=100 на трёх записях подтверждает допустимость параметра, но не ограничение результата на наборе больше 100 записей.
- PATCH-тесты проверяют статус и ID, но пока не проверяют сохранность всех остальных полей.
- После ошибок тела PATCH с кодом 422 отдельная проверка неизменности записи пока отсутствует.
- Повтор текущего статуса проверяется для processing.
- Последующий GET использует общую тестовую ORM-сессию и не является отдельной проверкой фиксации изменений через независимое подключение.
- TestClient не исполняет JavaScript формы. Её отправка и отображение сообщений проверяются отдельно в браузере.