-- 1
select u.name, a.user_id from day10.users as u left join day10.applications as a on a.user_id = u.id where a.id is null;
-- 2
select e.title, count(a.event_id) from day10.events as e left join day10.applications as a on a.event_id = e.id group by e.title, a.event_id;
-- 3
select u.name, e.title from day10.users as u left join day10.applications as a on u.id = a.user_id left join day10.events as e on a.event_id = e.id where status = 'done';
-- 4
select a.status, count(*) from day10.applications as a group by a.status;
-- 5
select p.status, count(*) from day10.perf_test as p group by status having count(*) > 10000;
-- 6
select a.user_id, u.name ,count(a.user_id) from day10.users as u left join day10.applications as a on a.user_id = u.id group by a.user_id, u.name having count(*) > 1;
-- 7
with cnt as (
    select event_id, count(*) as n
    from day10.applications
    group by event_id
)
select e.title, coalesce(cnt.n, 0) as cnt
from day10.events as e
left join cnt on cnt.event_id = e.id
order by cnt desc limit 1;
-- 8
select u.name, a.id from day10.users as u left join day10.applications as a on a.user_id = u.id where a.id in (select max(a.id) from day10.applications as a group by a.user_id);
-- 9
select u.id, u.name, a.status from day10.users as u left join day10.applications as a on u.id = a.user_id group by u.name, u.id, a.status having a.status = 'new';
-- 10
BEGIN;

WITH upd AS (
    UPDATE day10.events
    SET seats_left = seats_left - 1
    WHERE id = 3 AND seats_left > 0
    RETURNING id
)
INSERT INTO day10.applications (user_id, event_id)
SELECT 2, id FROM upd;

SELECT * FROM day10.applications ORDER BY id;
SELECT id, seats_left FROM day10.events WHERE id = 3;

ROLLBACK;