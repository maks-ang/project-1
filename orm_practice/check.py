from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from orm_practice.models import User, Event, Application

engine = create_engine('postgresql+psycopg://n0tthesame@localhost:5432/sql_practice', echo=True)

with Session(engine) as session:
    users = session.scalars(select(User)).all()
    for user in users:
        print(user.id, user.name, user.email, len(user.applications))
    user = session.get(User, 1)
    session.add(User(name='тест', email='something@gmail.com'))
    session.flush()
    session.rollback()


# session.scalars(select(User)).all() - select * from day10.users;
# session.get(User, 1) — SQL не выполнялся: пользователь 1 уже загружен в сессию предыдущим select, session.get взял его из identity map
# user.applications - select * from day10.applications where user_id = ...; создаётся запрос на каждого юзера отдельно
