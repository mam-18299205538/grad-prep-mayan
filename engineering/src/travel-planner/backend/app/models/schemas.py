"""前后端共用的旅行规划数据契约。"""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class TripRequest(BaseModel):
    city: str = Field(..., min_length=1, max_length=50, description="目的地城市")
    start_date: str = Field(..., description="开始日期 YYYY-MM-DD")
    end_date: str = Field(..., description="结束日期 YYYY-MM-DD")
    travel_days: int = Field(..., ge=1, le=14, description="旅行天数")
    transportation: str = Field(..., min_length=1, max_length=30, description="交通方式")
    accommodation: str = Field(..., min_length=1, max_length=30, description="住宿偏好")
    preferences: List[str] = Field(default_factory=list, max_length=8, description="旅行偏好")
    free_text_input: str = Field(default="", max_length=500, description="额外要求")

    @field_validator("city")
    @classmethod
    def strip_city(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("目的地城市不能为空")
        return value

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_iso_date(cls, value: str) -> str:
        try:
            return date.fromisoformat(value).isoformat()
        except ValueError as error:
            raise ValueError("日期必须使用 YYYY-MM-DD 格式") from error

    @model_validator(mode="after")
    def validate_trip_range(self) -> "TripRequest":
        start = date.fromisoformat(self.start_date)
        end = date.fromisoformat(self.end_date)
        actual_days = (end - start).days + 1
        if actual_days < 1:
            raise ValueError("结束日期不能早于开始日期")
        if actual_days != self.travel_days:
            raise ValueError("旅行天数必须与开始、结束日期一致")
        return self


class POISearchRequest(BaseModel):
    keywords: str = Field(..., min_length=1, max_length=80)
    city: str = Field(..., min_length=1, max_length=50)
    citylimit: bool = True


class RouteRequest(BaseModel):
    origin_address: str = Field(..., min_length=1)
    destination_address: str = Field(..., min_length=1)
    origin_city: Optional[str] = None
    destination_city: Optional[str] = None
    route_type: str = Field(default="walking", pattern="^(walking|driving|transit)$")


class Location(BaseModel):
    longitude: float = Field(..., ge=-180, le=180)
    latitude: float = Field(..., ge=-90, le=90)


class Attraction(BaseModel):
    name: str
    address: str
    location: Location
    visit_duration: int = Field(..., gt=0, le=720)
    description: str
    category: str = "景点"
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    photos: List[str] = Field(default_factory=list)
    poi_id: str = ""
    image_url: Optional[str] = None
    ticket_price: int = Field(default=0, ge=0)


class Meal(BaseModel):
    type: str
    name: str
    address: Optional[str] = None
    location: Optional[Location] = None
    description: Optional[str] = None
    estimated_cost: int = Field(default=0, ge=0)


class Hotel(BaseModel):
    name: str
    address: str = ""
    location: Optional[Location] = None
    price_range: str = ""
    rating: str = ""
    distance: str = ""
    type: str = ""
    estimated_cost: int = Field(default=0, ge=0)


class DayPlan(BaseModel):
    date: str
    day_index: int = Field(..., ge=0)
    description: str
    transportation: str
    accommodation: str
    hotel: Optional[Hotel] = None
    attractions: List[Attraction] = Field(default_factory=list)
    meals: List[Meal] = Field(default_factory=list)


class WeatherInfo(BaseModel):
    date: str
    day_weather: str = ""
    night_weather: str = ""
    day_temp: int = 0
    night_temp: int = 0
    wind_direction: str = ""
    wind_power: str = ""

    @field_validator("day_temp", "night_temp", mode="before")
    @classmethod
    def parse_temperature(cls, value: object) -> int:
        if isinstance(value, str):
            value = value.replace("°C", "").replace("℃", "").replace("°", "").strip()
        try:
            return int(value)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return 0


class Budget(BaseModel):
    total_attractions: int = Field(default=0, ge=0)
    total_hotels: int = Field(default=0, ge=0)
    total_meals: int = Field(default=0, ge=0)
    total_transportation: int = Field(default=0, ge=0)
    total: int = Field(default=0, ge=0)


class TripPlan(BaseModel):
    city: str
    start_date: str
    end_date: str
    days: List[DayPlan] = Field(default_factory=list)
    weather_info: List[WeatherInfo] = Field(default_factory=list)
    overall_suggestions: str
    budget: Optional[Budget] = None


class TripPlanResponse(BaseModel):
    success: bool
    message: str = ""
    mode: str = "mock"
    data: Optional[TripPlan] = None


class POIInfo(BaseModel):
    id: str
    name: str
    type: str
    address: str
    location: Location
    tel: Optional[str] = None


class POISearchResponse(BaseModel):
    success: bool
    message: str = ""
    data: List[POIInfo] = Field(default_factory=list)


class RouteInfo(BaseModel):
    distance: float
    duration: int
    route_type: str
    description: str


class RouteResponse(BaseModel):
    success: bool
    message: str = ""
    data: Optional[RouteInfo] = None


class WeatherResponse(BaseModel):
    success: bool
    message: str = ""
    data: List[WeatherInfo] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
