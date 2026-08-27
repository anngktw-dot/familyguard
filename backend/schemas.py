from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CheckInRequest(BaseModel):
    status: str = Field(min_length=1, max_length=80)
    location_label: str = Field(default="Not shared", max_length=120)
    battery_percent: int = Field(default=100, ge=0, le=100)

    @field_validator("status", "location_label")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class UsageUpdateRequest(BaseModel):
    screen_time_minutes: int = Field(ge=0, le=24 * 60)
    top_apps: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("top_apps")
    @classmethod
    def normalize_apps(cls, apps: list[str]) -> list[str]:
        cleaned = [app.strip() for app in apps if app.strip()]
        return cleaned[:10]


class ChildRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: str
    location_label: str
    battery_percent: int
    screen_time_minutes: int
    top_apps: list[str]
    last_check_in: datetime
