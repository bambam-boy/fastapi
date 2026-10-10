from pydantic_settings import SettingsConfigDict, BaseSettings


class Configs(BaseSettings):
    DB_HOST:str
    DB_PORT:str
    DB_USERNAME:str
    DB_PASSWORD:str
    DB_PATH:str



    API_PATH:str="/api"
    PROJECT_TITLE:str="website"

    
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )



settings=Configs()