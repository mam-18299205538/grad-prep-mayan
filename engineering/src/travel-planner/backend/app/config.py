"""应用配置与运行模式管理。"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env")


class Settings(BaseSettings):
    """从环境变量读取配置；默认使用不依赖外部密钥的演示模式。"""

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "HelloAgents 智能旅行助手"
    app_version: str = "1.1.0"
    app_mode: str = "mock"  # mock 或 live
    debug: bool = False

    host: str = "127.0.0.1"
    port: int = 8000
    cors_origins: str = (
        "http://localhost:5173,http://127.0.0.1:5173,"
        "http://localhost:5174,http://127.0.0.1:5174,"
        "http://localhost:3000,http://127.0.0.1:3000"
    )

    amap_api_key: str = ""
    amap_mcp_command: str = "uvx"  # uvx 或 npx
    unsplash_access_key: str = ""
    unsplash_secret_key: str = ""

    llm_api_key: str = ""
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model_id: str = ""
    llm_timeout: int = 90
    log_level: str = "INFO"

    @property
    def is_live_mode(self) -> bool:
        return self.app_mode.strip().lower() == "live"

    def get_cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()


def get_settings() -> Settings:
    return settings


def get_amap_mcp_server_command() -> list[str]:
    """返回可在当前开发环境中实际启动的高德 MCP 命令。"""
    if settings.amap_mcp_command.strip().lower() == "npx":
        return ["npx", "-y", "@sugarforever/amap-mcp-server"]

    # 直接使用项目虚拟环境中的 uvx，避免通过 python.exe 启动后 PATH 中找不到 uvx。
    local_uvx = BACKEND_DIR / ".venv" / "Scripts" / ("uvx.exe" if os.name == "nt" else "uvx")
    if local_uvx.exists():
        return [str(local_uvx), "amap-mcp-server"]
    return ["uvx", "amap-mcp-server"]


def validate_config() -> list[str]:
    """校验配置并返回提示信息；Mock 模式不将缺失密钥视为启动错误。"""
    if settings.app_mode.strip().lower() not in {"mock", "live"}:
        raise ValueError("APP_MODE 只能是 mock 或 live")

    notices: list[str] = []
    if settings.is_live_mode:
        if not settings.amap_api_key:
            raise ValueError("Live 模式需要配置 AMAP_API_KEY")
        if not (settings.llm_api_key or os.getenv("OPENAI_API_KEY")):
            raise ValueError("Live 模式需要配置 LLM_API_KEY 或 OPENAI_API_KEY")
        notices.append("已启用真实 LLM 与高德 MCP 服务")
    else:
        notices.append("当前为 Mock 演示模式：未使用任何外部 API Key")
    return notices


def print_config() -> None:
    print(f"应用名称: {settings.app_name}")
    print(f"版本: {settings.app_version}")
    print(f"运行模式: {settings.app_mode}")
    print(f"服务器: {settings.host}:{settings.port}")
    print(f"高德地图 Key: {'已配置' if settings.amap_api_key else '未配置'}")
    print(f"LLM Key: {'已配置' if settings.llm_api_key or os.getenv('OPENAI_API_KEY') else '未配置'}")
