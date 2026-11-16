from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from orm_practice.models import User, Event, Application

engine = create_engine('postgresql+psycopg://n0tthesame@localhost:5432/sql_practice', echo=True)
with Session(engine) as session:
    applications = session.scalars(select(Application)).all()
    for application in applications:
        print(application.id, application.user_id, application.event_id, application.status)
    app = Application(user_id=4, event_id=1, status='new')
    session.add(app)
    session.flush()
    session.rollback()

    app = session.get(Application, 1)
    app.status = 'processing'
    session.flush()
    session.rollback()

    app = session.get(Application, 1)
    session.delete(app)
    session.flush()
    session.rollback()

    # app = Application(user_id=1, event_id=1, status='new')
    # session.add(app)
    # session.flush()
    # session.rollback()

    rows = session.execute(
        select(User.name, Application.status).join(User.applications).where(Application.status == 'new')).all()
    print(rows)

    session.add(User(name='Тестовый юзер', email='test@mail.ru'))
    session.flush()
    rows = session.execute(select(User.name, Application.status).outerjoin(User.applications)).all()
    print(rows)
    session.rollback()

    result = session.execute(
        select(Application.id, User.name, Event.title).join(Application.user).join(Application.event).where(
            Application.status == 'new').order_by(Application.id).limit(2).offset(2)).all()
    print(result)
