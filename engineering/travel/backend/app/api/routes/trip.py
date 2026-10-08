"""旅行规划 API。"""

from fastapi import APIRouter, HTTPException

from ...config import get_settings
from ...models.schemas import TripPlanResponse, TripRequest
from ...services.planner_service import create_trip_plan


router = APIRouter(prefix="/trip", tags=["旅行规划"])


@router.post("/plan", response_model=TripPlanResponse, summary="生成旅行计划")
async def plan_trip(request: TripRequest) -> TripPlanResponse:
    settings = get_settings()
    try:
        trip_plan = create_trip_plan(request)
        mode_label = "真实服务" if settings.is_live_mode else "演示模式"
        return TripPlanResponse(
            success=True,
            mode=settings.app_mode,
            message=f"{mode_label}已生成 {request.city} {request.travel_days} 日旅行计划",
            data=trip_plan,
        )
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"旅行计划生成失败：{error}") from error


@router.get("/health", summary="旅行规划服务状态")
async def health_check() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "healthy",
        "service": "trip-planner",
        "mode": settings.app_mode,
    }
