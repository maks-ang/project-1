from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
import pytest
from orm_practice.booking import book_event
from orm_practice.models import User, Event, Application


def test_booking_no_seats(db_session, event, user):
    event.seats_left = 0
    db_session.flush()
    seats_before = db_session.scalar(select(Event.seats_left).where(Event.id == event.id))
    with pytest.raises(ValueError):
        book_event(db_session, event_id=event.id, user_id=user.id)
    seats_after = db_session.scalar(select(Event.seats_left).where(Event.id == event.id))

    assert seats_before == seats_after


def test_booking_uniq_event(db_session, event, user):
    db_session.add(Application(user_id=user.id, event_id=event.id, status="new"))
    db_session.flush()
    seats_before = db_session.scalar(select(Event.seats_left).where(Event.id == event.id))
    with pytest.raises(IntegrityError):
        with db_session.begin_nested():
            book_event(db_session, event_id=event.id, user_id=user.id)
    seats_after = db_session.scalar(select(Event.seats_left).where(Event.id == event.id))

    assert seats_before == seats_after


def test_seats_negative(db_session):
    db_session.add(Event(title="тест", seats_left=-1))
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_application_status_valid(db_session, user, event):
    db_session.add(Application(user_id=user.id, event_id=event.id, status="rejected"))
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_application_uniq_event(db_session, event, user):
    db_session.add(Application(user_id=user.id, event_id=event.id, status="new"))
    db_session.add(Application(user_id=user.id, event_id=event.id, status="new"))
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_application_no_user(db_session, user, event):
    db_session.add(Application(user_id=9999, event_id=event.id,status='new'))
    with pytest.raises(IntegrityError):
        db_session.flush()


def test_event_no_title(db_session, event):
    db_session.add(Event(seats_left=1))
    with pytest.raises(IntegrityError):
        db_session.flush()
