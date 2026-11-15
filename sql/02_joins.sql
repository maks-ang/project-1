select * from day10.applications inner join day10.users on day10.applications.user_id = day10.users.id; -- ожидаю 3 строки
select * from day10.applications inner join day10.events on day10.applications.event_id = day10.events.id; -- ожидаю 3 строки
select * from day10.events left join day10.applications on day10.applications.event_id = day10.events.id where applications.id is NULL; --ожидаю событие с id 4 так как на него нет заявок
select * from day10.users left join day10.applications on day10.applications.user_id = day10.users.id where applications.id is NULL; --ожидаю пользователя с id 4 так как у него не заявок на ивенты
select * from day10.users left join day10.applications on day10.applications.user_id = day10.users.id where day10.applications.event_id = 1; -- ожидаю две строки так как на событие 1 есть две заявки
select event_id from day10.applications group by event_id having count(applications.id) >= 2; --ожидаю 1 строку с id 1
select day10.applications.id, day10.users.name, day10.events.title from day10.applications inner join day10.users on day10.applications.user_id = day10.users.id inner join day10.events on day10.applications.event_id = day10.events.id; --ожидаю 3 строки
select * from day10.users where not exists (select 1 from day10.applications where day10.applications.user_id = day10.users.id); --ожидаю 1 строку юзер с id 4 у него нет заявок
SELECT * FROM day10.users CROSS JOIN day10.events; --ожидаю 9 строк потому что тут считается как n*m строки таблицы
SELECT * FROM day10.users CROSS JOIN day10.applications WHERE day10.applications.id IS NULL;
SELECT * FROM day10.users CROSS JOIN day10.events WHERE day10.users.id = day10.events.id;
select * from day10.users as users CROSS JOIN applications WHERE applications.id IS NULL;
select * from day10.events as events LEFT JOIN day10.applications as applications ON applications.event_id = events.id AND applications.status = 'approved';
select * from day10.users as users LEFT JOIN day10.applications as applications ON applications.user_id = users.id AND applications.status = 'approved';