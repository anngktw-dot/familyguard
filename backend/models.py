from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.db import Base


class Child(Base):
    __tablename__ = "children"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(80), nullable=False, default="All good")
    location_label: Mapped[str] = mapped_column(
        String(120), nullable=False, default="Not shared"
    )
    battery_percent: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    screen_time_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    top_apps: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    last_check_in: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
