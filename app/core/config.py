from pydantic_settings import SettingsConfigDict, BaseSettings


class Configs(BaseSettings):

    
    
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="uft-8"
    )



settings=Configs()