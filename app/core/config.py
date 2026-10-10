from pydantic_settings import SettingsConfigDict, BaseSettings


class Configs(BaseSettings):
    DB_HOST:str
    DB_PORT:str
    DB_USERNAME:str
    DB_PASSWORD:str
    DB_PATH:str

    
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="uft-8"
    )



settings=Configs()