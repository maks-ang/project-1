from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
import pytest
from orm_practice.booking import book_event
from orm_practice.models import User, Event, Application


def test_booking_no_seats(session):
    seats_before = session.scalar(select(Event.seats_left).where(Event.id == 4))
    with pytest.raises(ValueError):
        book_event(session, event_id=4, user_id=4)
    seats_after = session.scalar(select(Event.seats_left).where(Event.id == 4))

    assert seats_before == seats_after


def test_booking_uniq_event(session):
    seats_before = session.scalar(select(Event.seats_left).where(Event.id == 1))
    with pytest.raises(IntegrityError):
        book_event(session, event_id=1, user_id=1)
    session.rollback()
    seats_after = session.scalar(select(Event.seats_left).where(Event.id == 1))

    assert seats_before == seats_after
