from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    order_details: Mapped[str] = mapped_column(Text, nullable=False)
