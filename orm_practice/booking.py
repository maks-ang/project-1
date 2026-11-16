from sqlalchemy import update
from sqlalchemy.orm import Session
from orm_practice.models import User, Event, Application


def book_event(session: Session, event_id: int, user_id: int) -> None:
    result = session.execute(
        update(Event).where(Event.id == event_id, Event.seats_left > 0).values(seats_left=Event.seats_left - 1))
    if result.rowcount == 0:
        raise ValueError('На событие не осталось мест')
    session.add(Application(event_id=event_id, user_id=user_id))
    session.commit()
