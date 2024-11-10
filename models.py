from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from main import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Url(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    original_url: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    short_url: Mapped[str] = mapped_column(String(6), unique=True, nullable=False)
