from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import (
     ValidationInfo,
     field_validator,
     PostgresDsn,
     SecretStr
)


class Configs(BaseSettings):
    DB_HOST:str
    DB_PORT:str
    DB_USERNAME:str
    DB_PASSWORD:str
    DB_PATH:str
    SECRET_KEY:SecretStr

    ALGORITHM:str="HS256"
    exp_token_min:int=360

    REDIS_URL:str

    API_PATH:str="/api"
    PROJECT_TITLE:str="website"

    SQLALCHEMY_URL_ASYNC:str=""


    @field_validator("SQLALCHEMY_URL_ASYNC",mode="before")
    def attach_url(cls,v:str,value:ValidationInfo)->str:
        if not v is None and not v =="":
            return v
        datas=value.data
        url=PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=datas["DB_HOST"],
            port=int(datas["DB_PORT"]),
            username=datas["DB_USERNAME"],
            password=datas["DB_PASSWORD"],
            path=datas["DB_PATH"]
        ).encoded_string()

        return url
        

    
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )



settings=Configs()