select event_id, count(event_id) from day10.applications group by event_id; --ожидал 2 строки потому то на событие 4 заявок 0 --получил 2 строки
select event_id, count(event_id) from day10.applications group by event_id having count(event_id) >= 2; --ожидал 1 строку потому что только на событие 1 заявок 2 или больше
select user_id, count(user_id) from day10.applications group by user_id having count(user_id) >= 2; --ожидал 1 строку потому что только пользователь 1 имеет 2 или больше заявки
select day10.events.id, count(applications.id) from day10.events left join day10.applications on day10.events.id = day10.applications.event_id group by day10.events.id; --ожидал 3 строки потому что выведется каждое событие и сколько на него заявко даже те у кого 0
select day10.events.id, count(applications.id) from day10.events left join day10.applications on day10.events.id = day10.applications.event_id group by day10.events.id having count(applications.id) = 0; --ожидал 1 строку потому что на событие 4 ноль заявок

select day10.users.name, count(day10.applications.id) from day10.users left join day10.applications on day10.users.id = day10.applications.user_id group by day10.users.id; --ожидаю 3 строки имя каждого юзера и его количество заявок
select day10.events.title, count(applications.id) from day10.events left join day10.applications on day10.events.id = day10.applications.event_id group by day10.events.id having count(applications.id) > 0; --ожидаю 2 строки это ивенты на которые есть 1 или больше заявки
select count(distinct day10.applications.user_id) from day10.applications; --ожидаю 1 строку с количеством 2 (юзеры которые подали 1 или больше заявок)
select day10.users.name, day10.users.email from day10.users left join day10.applications on day10.users.id = day10.applications.user_id group by day10.users.id having count(applications.id) = 1; --ожидаю 1 строку так как юзер 2 имеет одну заявку
select day10.events.id, day10.events.title, count(distinct day10.applications.user_id), count(applications.id) from day10.events left join day10.applications on day10.events.id = day10.applications.event_id group by day10.events.id having count(applications.id) > 0; --ожидаю 2 строки это ивенты на которые есть заявки и кол-во юзеров которые подали на этот ивент
select day10.users.id, day10.users.name, day10.events.title from day10.users inner join day10.applications on day10.users.id = day10.applications.user_id inner join day10.events on day10.events.id = day10.applications.event_id where day10.applications.status = 'new' order by day10.events.title desc; --ожидаю 3 строки потому что заявок у нас 3 и выводим каждого юзера и куда он подал на какой ивент заявку
select day10.users.id, day10.users.name, day10.events.title from day10.users cross join day10.events left join day10.applications on day10.users.id = day10.applications.user_id and day10.events.id = day10.applications.event_id where day10.applications.id is NULL; --ожидаю 6 строк пары которые не имеют заявок
select day10.events.title, count(day10.applications.id) from day10.events left join day10.applications on day10.events.id = day10.applications.event_id group by day10.events.id order by count desc limit 1; --ожидаю 1 заявку с максимальным количеством заявок
select day10.users.name, count(distinct day10.applications.event_id) from day10.users left join day10.applications on day10.users.id = day10.applications.user_id group by day10.users.id having count(distinct day10.applications.event_id) > 1; --ожидаю 1 заявку с количеством заявок больше 2
select day10.events.id, day10.events.title, count(day10.users.id) from day10.events left join day10.applications on day10.events.id = day10.applications.event_id left join day10.users on day10.users.id = day10.applications.user_id and day10.users.name = 'Макс' group by day10.events.id; --ожидаю 3 строки ивенты и количество юзеров которые подали на них заявки с именем Макс
SELECT day10.users.name,
       (SELECT COUNT(*) FROM day10.applications
        WHERE day10.applications.user_id = day10.users.id)
FROM day10.users;
WITH cnt AS (
  SELECT user_id, COUNT(*) AS n
  FROM day10.applications
  GROUP BY user_id
)
SELECT u.name, COALESCE(c.n, 0) AS cnt
FROM day10.users AS u
LEFT JOIN cnt AS c ON c.user_id = u.id;