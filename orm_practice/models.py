from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"schema": "day10"}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text)
    applications: Mapped[list["Application"]] = relationship(back_populates="user")


class Event(Base):
    __tablename__ = 'events'
    __table_args__ = {"schema": "day10"}

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    seats_left: Mapped[int] = mapped_column(Integer)
    applications: Mapped[list["Application"]] = relationship(back_populates="event")


class Application(Base):
    __tablename__ = 'applications'
    __table_args__ = {"schema": "day10"}

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    event_id: Mapped[int] = mapped_column(ForeignKey(Event.id))
    status: Mapped[str] = mapped_column(Text, default="new")
    user: Mapped[User] = relationship(back_populates="applications")
    event: Mapped[Event] = relationship(back_populates="applications")

# sqlalchemy.exc.ArgumentError: Mapper Mapper[Application(applications)] could not assemble any primary key columns for mapped table 'applications'
# ошибка primary key стоит False а не True
# user_id: Mapped[int] = mapped_column(ForeignKey(Users.id))
# NameError: name 'Users' is not defined. Did you mean: 'User'? — Users не объявлен, класс называется User; ошибка при импорте, до обращения к базе
# sqlalchemy.exc.ProgrammingError: (psycopg.errors.UndefinedTable) relation "day10.random" does not exist
# ошибка таблицы с именем random не найдена
# sqlalchemy.exc.ProgrammingError: (psycopg.errors.UndefinedTable) relation "public.users" does not exist
# ошибка неверная схема указана
# sqlalchemy.exc.ProgrammingError: (psycopg.errors.UndefinedColumn) column users.error does not exist
# ошибка неверное имя колонки error вместо name
