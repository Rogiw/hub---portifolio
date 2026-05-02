from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "Wigor Rodrigues API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"
    public_api_url: str = "https://api.wigorrodrigues.com.br"
    allowed_origins: tuple[str, ...] = (
        "https://wigorrodrigues.com.br",
        "https://www.wigorrodrigues.com.br",
        "http://localhost:3000",
        "http://localhost:5173",
    )


settings = Settings()
