from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, selectinload
from orm_practice.models import User, Event, Application

engine = create_engine('postgresql+psycopg://n0tthesame@localhost:5432/sql_practice', echo=True)

with Session(engine) as session:
    users = session.scalars(select(User).options(selectinload(User.applications))).all()
    for user in users:
        print(user.id, user.name, user.email, len(user.applications))
