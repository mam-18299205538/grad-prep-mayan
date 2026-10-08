"""高德地图服务适配层；Mock 模式提供可联调的本地结果。"""

from __future__ import annotations

import json
from typing import Any, Optional

from ..config import get_amap_mcp_server_command, get_settings
from ..models.schemas import Location, POIInfo, RouteInfo, WeatherInfo
from .mock_travel_service import mock_route, mock_weather, search_mock_poi


_amap_service: Optional["AmapService"] = None


class AmapService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.mcp_tool: Any = None
        if self.settings.is_live_mode:
            self.mcp_tool = self._create_mcp_tool()

    def _create_mcp_tool(self) -> Any:
        try:
            from hello_agents.tools import MCPTool
        except ImportError as error:
            raise RuntimeError(
                "真实模式需要安装 requirements-live.txt 中的 HelloAgents 依赖"
            ) from error

        return MCPTool(
            name="amap",
            description="高德地图服务，支持 POI、天气和路线查询",
            server_command=get_amap_mcp_server_command(),
            env={"AMAP_MAPS_API_KEY": self.settings.amap_api_key},
            auto_expand=True,
        )

    def _call_live_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
        if not self.mcp_tool:
            raise RuntimeError("高德 MCP 尚未初始化")
        result = self.mcp_tool.run(
            {"action": "call_tool", "tool_name": tool_name, "arguments": arguments}
        )
        return str(result)

    @staticmethod
    def _extract_json(text: str) -> Any:
        decoder = json.JSONDecoder()
        for index, character in enumerate(text):
            if character not in "[{":
                continue
            try:
                payload, _ = decoder.raw_decode(text[index:])
                return payload
            except json.JSONDecodeError:
                continue
        return None

    @staticmethod
    def _as_float(value: Any, default: float = 0.0) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _as_int(value: Any, default: int = 0) -> int:
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _parse_location(value: Any) -> Optional[Location]:
        parts = str(value or "").split(",")
        if len(parts) != 2:
            return None
        try:
            return Location(longitude=float(parts[0]), latitude=float(parts[1]))
        except (TypeError, ValueError):
            return None

    def search_poi(self, keywords: str, city: str, citylimit: bool = True) -> list[POIInfo]:
        if not self.settings.is_live_mode:
            return search_mock_poi(keywords, city)

        raw = self._call_live_tool(
            "maps_text_search",
            {"keywords": keywords, "city": city, "citylimit": str(citylimit).lower()},
        )
        payload = self._extract_json(raw)
        # 文本搜索结果默认可达 20 条，但 amap-mcp-server 省略坐标；
        # 只为前 10 条调用详情工具补坐标，避免一次搜索触发过多串行 MCP 请求。
        items = payload.get("pois", [])[:10] if isinstance(payload, dict) else []
        results: list[POIInfo] = []
        for item in items:
            location = self._parse_location(item.get("location"))
            if location is None and item.get("id"):
                detail = self.get_poi_detail(str(item["id"]))
                location = self._parse_location(detail.get("location"))
            if location is None:
                # 详情无坐标时，再用地址地理编码兜底。
                address = str(item.get("address", "")).strip()
                location = self.geocode(address, city) if address else None
            if location is None:
                continue
            try:
                results.append(
                    POIInfo(
                        id=str(item.get("id", "")),
                        name=str(item.get("name", "")),
                        type=str(item.get("type") or item.get("typecode") or "景点"),
                        address=str(item.get("address", "")),
                        location=location,
                        tel=item.get("tel"),
                    )
                )
            except (TypeError, ValueError):
                continue
        return results

    def get_weather(self, city: str) -> list[WeatherInfo]:
        if not self.settings.is_live_mode:
            return mock_weather(city)

        raw = self._call_live_tool("maps_weather", {"city": city})
        payload = self._extract_json(raw)
        forecasts = payload.get("forecasts", []) if isinstance(payload, dict) else []
        return [
            WeatherInfo(
                date=str(forecast.get("date", "")),
                day_weather=str(forecast.get("day_weather") or forecast.get("dayweather", "")),
                night_weather=str(forecast.get("night_weather") or forecast.get("nightweather", "")),
                day_temp=self._as_int(forecast.get("day_temp") or forecast.get("daytemp")),
                night_temp=self._as_int(forecast.get("night_temp") or forecast.get("nighttemp")),
                wind_direction=str(forecast.get("wind_direction") or forecast.get("daywind", "")),
                wind_power=str(forecast.get("wind_power") or forecast.get("daypower", "")),
            )
            for forecast in forecasts
            if isinstance(forecast, dict)
        ]

    def plan_route(
        self,
        origin_address: str,
        destination_address: str,
        origin_city: Optional[str] = None,
        destination_city: Optional[str] = None,
        route_type: str = "walking",
    ) -> RouteInfo:
        if not self.settings.is_live_mode:
            return mock_route(origin_address, destination_address, route_type)

        tool_name = {
            "walking": "maps_direction_walking_by_address",
            "driving": "maps_direction_driving_by_address",
            "transit": "maps_direction_transit_integrated_by_address",
        }[route_type]
        arguments: dict[str, str] = {
            "origin_address": origin_address,
            "destination_address": destination_address,
        }
        if origin_city:
            arguments["origin_city"] = origin_city
        if destination_city:
            arguments["destination_city"] = destination_city
        raw = self._call_live_tool(tool_name, arguments)
        payload = self._extract_json(raw)
        route = payload.get("route", {}) if isinstance(payload, dict) else {}
        paths = route.get("paths", []) if isinstance(route, dict) else []
        path = paths[0] if paths and isinstance(paths[0], dict) else route
        distance = self._as_float(path.get("distance")) if isinstance(path, dict) else 0.0
        duration = self._as_int(path.get("duration")) if isinstance(path, dict) else 0
        description = ""
        if isinstance(path, dict):
            steps = path.get("steps", [])
            instructions = [
                str(step.get("instruction", "")).strip()
                for step in steps
                if isinstance(step, dict) and step.get("instruction")
            ]
            description = "；".join(instructions[:3])
        return RouteInfo(
            distance=distance,
            duration=duration,
            route_type=route_type,
            description=description or str(route.get("description") or raw[:200]),
        )

    def geocode(self, address: str, city: Optional[str] = None) -> Optional[Location]:
        if not self.settings.is_live_mode:
            return None
        arguments = {"address": address}
        if city:
            arguments["city"] = city
        raw = self._call_live_tool("maps_geo", arguments)
        payload = self._extract_json(raw)
        geocodes = []
        if isinstance(payload, dict):
            geocodes = payload.get("geocodes") or payload.get("return") or []
        if not geocodes:
            return None
        location = str(geocodes[0].get("location", "")).split(",")
        if len(location) != 2:
            return None
        return Location(longitude=float(location[0]), latitude=float(location[1]))

    def get_poi_detail(self, poi_id: str) -> dict[str, Any]:
        if not self.settings.is_live_mode:
            return {"id": poi_id, "message": "演示模式不请求远程 POI 详情"}
        raw = self._call_live_tool("maps_search_detail", {"id": poi_id})
        return self._extract_json(raw) or {"raw": raw}


def get_amap_service() -> AmapService:
    global _amap_service
    if _amap_service is None:
        _amap_service = AmapService()
    return _amap_service
