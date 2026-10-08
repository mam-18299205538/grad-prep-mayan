"""无需外部密钥即可运行的确定性演示数据服务。"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Iterable

from ..models.schemas import (
    Attraction,
    Budget,
    DayPlan,
    Hotel,
    Location,
    Meal,
    POIInfo,
    RouteInfo,
    TripPlan,
    TripRequest,
    WeatherInfo,
)


def _attraction(
    name: str,
    address: str,
    longitude: float,
    latitude: float,
    description: str,
    ticket_price: int,
    category: str = "人文景观",
    duration: int = 120,
) -> Attraction:
    return Attraction(
        name=name,
        address=address,
        location=Location(longitude=longitude, latitude=latitude),
        visit_duration=duration,
        description=description,
        category=category,
        rating=4.7,
        ticket_price=ticket_price,
    )


CITY_ATTRACTIONS: dict[str, list[Attraction]] = {
    "北京": [
        _attraction("故宫博物院", "北京市东城区景山前街4号", 116.3970, 39.9180, "沿中轴线感受皇家建筑与典藏。", 60),
        _attraction("天坛公园", "北京市东城区天坛东里甲1号", 116.4107, 39.8822, "适合上午漫步，欣赏圜丘与祈年殿。", 34),
        _attraction("中国国家博物馆", "北京市东城区东长安街16号", 116.4012, 39.9031, "展览丰富，建议提前预约并预留半天。", 0, "博物馆", 180),
        _attraction("颐和园", "北京市海淀区新建宫门路19号", 116.2749, 39.9995, "昆明湖与长廊适合慢游。", 30, "园林", 180),
        _attraction("什刹海", "北京市西城区什刹海", 116.3836, 39.9427, "傍晚适合散步与品尝京味小吃。", 0, "街区", 90),
        _attraction("798艺术区", "北京市朝阳区酒仙桥路4号", 116.4967, 39.9841, "画廊、设计店与咖啡馆集中。", 0, "艺术街区", 150),
    ],
    "上海": [
        _attraction("外滩", "上海市黄浦区中山东一路", 121.4903, 31.2417, "欣赏万国建筑群与浦江景观。", 0, "城市景观", 90),
        _attraction("豫园", "上海市黄浦区福佑路168号", 121.4928, 31.2272, "古典园林与老城厢风貌。", 40, "园林", 120),
        _attraction("上海博物馆", "上海市黄浦区人民大道201号", 121.4755, 31.2302, "中国古代艺术收藏丰富。", 0, "博物馆", 180),
        _attraction("武康路", "上海市徐汇区武康路", 121.4394, 31.2092, "适合漫步欣赏梧桐与近代建筑。", 0, "街区", 120),
        _attraction("田子坊", "上海市黄浦区泰康路210弄", 121.4667, 31.2099, "石库门里弄中的手作与小店。", 0, "街区", 120),
        _attraction("上海科技馆", "上海市浦东新区世纪大道2000号", 121.5476, 31.2215, "适合亲子与科技爱好者。", 45, "博物馆", 180),
    ],
    "成都": [
        _attraction("成都大熊猫繁育研究基地", "成都市成华区外北熊猫大道1375号", 104.1420, 30.7327, "建议清晨入园，观察熊猫进食活动。", 55, "自然教育", 180),
        _attraction("宽窄巷子", "成都市青羊区长顺街附近", 104.0553, 30.6694, "清代街巷与川味小吃集聚地。", 0, "街区", 120),
        _attraction("武侯祠", "成都市武侯区武侯祠大街231号", 104.0480, 30.6464, "三国文化主题古迹。", 50, "人文景观", 150),
        _attraction("杜甫草堂", "成都市青羊区青华路37号", 104.0226, 30.6618, "诗歌文化与园林相结合。", 50, "人文景观", 150),
        _attraction("锦里", "成都市武侯区武侯祠大街231号", 104.0488, 30.6467, "夜游与小吃体验的热门选择。", 0, "街区", 90),
        _attraction("人民公园", "成都市青羊区少城路12号", 104.0602, 30.6624, "喝盖碗茶，感受本地慢生活。", 0, "公园", 90),
    ],
}

DEFAULT_ATTRACTIONS = [
    _attraction("城市博物馆", "城市中心文化区", 116.4074, 39.9042, "了解目的地历史与城市脉络。", 0, "博物馆", 150),
    _attraction("中央公园", "城市中心绿地", 116.4174, 39.9142, "适合放松步行与拍照。", 0, "公园", 90),
    _attraction("历史文化街区", "城市老城区", 116.4274, 39.9242, "探索本地建筑与传统美食。", 0, "街区", 120),
    _attraction("城市观景台", "城市中心高点", 116.4374, 39.9342, "在傍晚观看城市天际线。", 50, "城市景观", 90),
]

WEATHER_CYCLE = [
    ("晴", "晴", 25, 15),
    ("多云", "多云", 23, 14),
    ("晴间多云", "晴", 26, 16),
    ("小雨", "阴", 21, 14),
]


def attractions_for(city: str) -> list[Attraction]:
    return [item.model_copy(deep=True) for item in CITY_ATTRACTIONS.get(city.strip(), DEFAULT_ATTRACTIONS)]


def build_mock_plan(request: TripRequest) -> TripPlan:
    """生成可编辑且预算可复算的确定性演示行程。"""
    start = date.fromisoformat(request.start_date)
    all_attractions = attractions_for(request.city)
    hotel_cost = {"经济型酒店": 320, "舒适型酒店": 520, "豪华酒店": 980, "民宿": 420}.get(request.accommodation, 450)
    transport_daily = {"步行": 20, "公共交通": 45, "自驾": 150, "混合": 85}.get(request.transportation, 60)

    days: list[DayPlan] = []
    weather: list[WeatherInfo] = []
    for index in range(request.travel_days):
        current_date = start + timedelta(days=index)
        selections = [
            all_attractions[(index * 2) % len(all_attractions)].model_copy(deep=True),
            all_attractions[(index * 2 + 1) % len(all_attractions)].model_copy(deep=True),
        ]
        day_weather, night_weather, day_temp, night_temp = WEATHER_CYCLE[index % len(WEATHER_CYCLE)]
        hotel = Hotel(
            name=f"{request.city}·{request.accommodation}推荐住宿",
            address=f"{request.city}市中心，便于前往当日景点",
            location=selections[0].location.model_copy(deep=True),
            price_range=f"约 {hotel_cost} 元/晚",
            rating="4.6",
            distance="距首个景点约 2 公里",
            type=request.accommodation,
            estimated_cost=hotel_cost,
        )
        meals = [
            Meal(type="breakfast", name=f"{request.city}本地早餐", description="选择酒店周边口碑店铺", estimated_cost=28),
            Meal(type="lunch", name=f"{request.city}特色午餐", description="安排在上午景点附近", estimated_cost=65),
            Meal(type="dinner", name=f"{request.city}风味晚餐", description="安排在傍晚活动区域", estimated_cost=88),
        ]
        days.append(
            DayPlan(
                date=current_date.isoformat(),
                day_index=index,
                description=f"第 {index + 1} 天以 {selections[0].category} 和 {selections[1].category} 体验为主，减少往返。",
                transportation=request.transportation,
                accommodation=request.accommodation,
                hotel=hotel,
                attractions=selections,
                meals=meals,
            )
        )
        weather.append(
            WeatherInfo(
                date=current_date.isoformat(),
                day_weather=day_weather,
                night_weather=night_weather,
                day_temp=day_temp,
                night_temp=night_temp,
                wind_direction="东南风",
                wind_power="1-3级",
            )
        )

    budget = calculate_budget(days, transport_daily * request.travel_days)
    preference_text = "、".join(request.preferences) if request.preferences else "城市漫游"
    suggestion = (
        f"这是 {request.city} {request.travel_days} 日{preference_text}主题行程。"
        "演示模式中的景点、预算与天气用于验证流程；出行前请以官方开放时间和实时交通为准。"
    )
    if request.free_text_input.strip():
        suggestion += f" 已记录你的额外要求：{request.free_text_input.strip()}。"

    return TripPlan(
        city=request.city,
        start_date=request.start_date,
        end_date=request.end_date,
        days=days,
        weather_info=weather,
        overall_suggestions=suggestion,
        budget=budget,
    )


def calculate_budget(days: Iterable[DayPlan], transportation_total: int = 0) -> Budget:
    day_list = list(days)
    attractions = sum(item.ticket_price for day in day_list for item in day.attractions)
    hotels = sum(day.hotel.estimated_cost for day in day_list if day.hotel)
    meals = sum(meal.estimated_cost for day in day_list for meal in day.meals)
    return Budget(
        total_attractions=attractions,
        total_hotels=hotels,
        total_meals=meals,
        total_transportation=max(0, transportation_total),
        total=attractions + hotels + meals + max(0, transportation_total),
    )


def search_mock_poi(keywords: str, city: str) -> list[POIInfo]:
    keyword = keywords.strip().lower()
    candidates = attractions_for(city)
    matched = [
        item for item in candidates
        if not keyword or keyword in item.name.lower() or keyword in item.category.lower() or keyword in item.description.lower()
    ]
    selected = matched or candidates[:5]
    return [
        POIInfo(
            id=f"mock-{city}-{index}",
            name=item.name,
            type=item.category,
            address=item.address,
            location=item.location,
        )
        for index, item in enumerate(selected[:10], start=1)
    ]


def mock_weather(city: str) -> list[WeatherInfo]:
    today = date.today()
    return [
        WeatherInfo(
            date=(today + timedelta(days=index)).isoformat(),
            day_weather=day_weather,
            night_weather=night_weather,
            day_temp=day_temp,
            night_temp=night_temp,
            wind_direction="东南风",
            wind_power="1-3级",
        )
        for index, (day_weather, night_weather, day_temp, night_temp) in enumerate(WEATHER_CYCLE[:4])
    ]


def mock_route(origin: str, destination: str, route_type: str) -> RouteInfo:
    mode_labels = {"walking": "步行", "driving": "驾车", "transit": "公共交通"}
    distance = {"walking": 1800.0, "driving": 6200.0, "transit": 7400.0}.get(route_type, 1800.0)
    duration = {"walking": 1500, "driving": 1200, "transit": 2100}.get(route_type, 1500)
    return RouteInfo(
        distance=distance,
        duration=duration,
        route_type=route_type,
        description=f"演示路线：从 {origin} 前往 {destination}，推荐{mode_labels.get(route_type, '步行')}出行。",
    )
