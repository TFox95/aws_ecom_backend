
from typing import List, Union, Optional, Any, Dict

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator, model_validator
from pydantic import PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    BACKEND_HOST: str
    BACKEND_PORT: int

    # Declare DATABASE_URI as Optional
    DATABASE_URI: Optional[PostgresDsn] = None
    DATABASE_ECHO: bool

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls,
                              v: Union[str, List[str]]
                              ) -> Union[List[str], str]:

        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @model_validator(mode="before")
    def validate_environment(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if not values.get("DATABASE_URI"):
            raise ValueError("DATABASE_URI must be provided")
        return values

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
