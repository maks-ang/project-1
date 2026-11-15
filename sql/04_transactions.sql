--begin;
--update day10.events
--set seats_left = seats_left - 1
--where id = 3;
--insert into day10.applications (user_id, event_id)
--values (4, 3);
--commit;
--select * from day10.applications;
--select * from day10.events;

--begin;
--update day10.events
--set seats_left = seats_left - 1
--where id = 3;
--insert into day10.applications (user_id, event_id)
--values (4, 99);
--rollback;
--select * from day10.applications;
--select * from day10.events;

begin;
insert into day10.applications(id, user_id, event_id)
OVERRIDING SYSTEM VALUE
values (1, 4, 1);
rollback;

begin;
insert into day10.applications(user_id, event_id)
values(99, 1);
rollback;

begin;
insert into day10.applications(user_id, event_id)
values(1,1);
rollback;

begin;
insert into day10.applications(user_id, event_id)
values(NULL,1);
rollback;

begin;
update day10.events
set seats_left = -1
where id = 3;
rollback;