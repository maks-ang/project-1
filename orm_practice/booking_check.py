from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from orm_practice.booking import book_event

engine = create_engine('postgresql+psycopg://n0tthesame@localhost:5432/sql_practice', echo=True)

with Session(engine) as session:
    try:
        book_event(session, event_id=4, user_id=4)
        print('Заявка отправлена')
    except ValueError as error:
        print('Ошибка:', error)
