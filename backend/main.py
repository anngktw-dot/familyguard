import os
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.db import Base, SessionLocal, engine, get_db
from backend.models import Child
from backend.schemas import CheckInRequest, ChildRead, UsageUpdateRequest

DbSession = Annotated[Session, Depends(get_db)]


def _seed_demo_child() -> None:
    with SessionLocal() as db:
        if db.get(Child, 1) is not None:
            return

        db.add(
            Child(
                id=1,
                name="Alex",
                status="All good",
                location_label="Home",
                battery_percent=86,
                screen_time_minutes=132,
                top_apps=["YouTube", "Maps", "Messages"],
                last_check_in=datetime.now(UTC),
            )
        )
        db.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    _seed_demo_child()
    yield


app = FastAPI(
    title="FamilyGuard API",
    version="1.1.0",
    description=(
        "Consent-first family safety demo API for explicit check-ins, shared status, "
        "battery information, and screen-time summaries."
    ),
    lifespan=lifespan,
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv("FAMILYGUARD_CORS_ORIGINS", "*").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


def _get_child_or_404(child_id: int, db: Session) -> Child:
    child = db.get(Child, child_id)
    if child is None:
        raise HTTPException(status_code=404, detail="Child not found")
    return child


@app.get("/", tags=["meta"])
def root() -> dict[str, str]:
    return {
        "name": "FamilyGuard API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/children", response_model=list[ChildRead], tags=["children"])
def list_children(db: DbSession) -> list[Child]:
    return list(db.scalars(select(Child).order_by(Child.id)).all())


@app.get("/children/{child_id}", response_model=ChildRead, tags=["children"])
def get_child(child_id: int, db: DbSession) -> Child:
    return _get_child_or_404(child_id, db)


@app.post(
    "/children/{child_id}/check-in",
    response_model=ChildRead,
    status_code=status.HTTP_200_OK,
    tags=["check-ins"],
)
def create_check_in(
    child_id: int,
    payload: CheckInRequest,
    db: DbSession,
) -> Child:
    child = _get_child_or_404(child_id, db)
    child.status = payload.status
    child.location_label = payload.location_label
    child.battery_percent = payload.battery_percent
    child.last_check_in = datetime.now(UTC)
    db.commit()
    db.refresh(child)
    return child


@app.post(
    "/children/{child_id}/usage",
    response_model=ChildRead,
    tags=["usage"],
)
def update_usage(
    child_id: int,
    payload: UsageUpdateRequest,
    db: DbSession,
) -> Child:
    child = _get_child_or_404(child_id, db)
    child.screen_time_minutes = payload.screen_time_minutes
    child.top_apps = payload.top_apps
    db.commit()
    db.refresh(child)
    return child
