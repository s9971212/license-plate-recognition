from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Branch(Base):
    __tablename__ = "branch"

    branch_id: Mapped[str] = mapped_column(
        String(10),
        primary_key=True,
    )

    branch_name: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    created_user: Mapped[str] = mapped_column(
        String(12),
        nullable=False,
    )

    created_date: Mapped[datetime] = mapped_column(
        default=datetime.now,
        nullable=False,
    )

    updated_user: Mapped[str] = mapped_column(
        String(12),
        nullable=True,
    )

    updated_date: Mapped[datetime] = mapped_column(
        nullable=True,
    )


class Gate(Base):
    __tablename__ = "gate"

    gate_id: Mapped[str] = mapped_column(
        String(10),
        primary_key=True,
    )

    gate_name: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    ip: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    created_user: Mapped[str] = mapped_column(
        String(12),
        nullable=False,
    )

    created_date: Mapped[datetime] = mapped_column(
        default=datetime.now,
        nullable=False,
    )

    updated_user: Mapped[str] = mapped_column(
        String(12),
        nullable=True,
    )

    updated_date: Mapped[datetime] = mapped_column(
        nullable=True,
    )

    branch_id: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
