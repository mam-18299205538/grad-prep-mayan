"""统一旅行规划入口，隔离 Mock 与真实多智能体实现。"""

from __future__ import annotations

from ..config import get_settings
from ..models.schemas import TripPlan, TripRequest
from .mock_travel_service import build_mock_plan, calculate_budget


def create_trip_plan(request: TripRequest) -> TripPlan:
    settings = get_settings()
    if not settings.is_live_mode:
        return build_mock_plan(request)

    # 仅在真实模式导入 HelloAgents，保证无 Key 的演示模式可独立启动。
    from ..agents.trip_planner_agent import get_trip_planner_agent

    plan = get_trip_planner_agent().plan_trip(request)
    transport_total = {"步行": 20, "公共交通": 45, "自驾": 150, "混合": 85}.get(request.transportation, 60)
    plan.budget = calculate_budget(plan.days, transport_total * request.travel_days)
    return plan
