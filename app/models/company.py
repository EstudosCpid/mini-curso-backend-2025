from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from app.settings.database import Base

class Company(Base):
    __tablename__ = "company"

    id: Mapped[BigInteger] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[String] = mapped_column(String(50), nullable=False)
    description: Mapped[String] = mapped_column(String(100))
    telephone: Mapped[String] = mapped_column(String(20))
    address: Mapped[String] = mapped_column(String(200))
