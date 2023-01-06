from os import getenv
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Facebook:
    app_id: str
    app_secret: str
    access_token: str
    adaccount_id: str
    form_ids: list[str]


@dataclass
class KeyCRM:
    api_token: str


@dataclass
class Script:
    debug: bool


@dataclass
class Config:
    facebook: Facebook
    script: Script
    keycrm: KeyCRM


def load_config(env_path: str = ".env") -> Config:
    load_dotenv(env_path)

    return Config(
        facebook=Facebook(
            app_id=getenv("APP_ID", ""),
            app_secret=getenv("APP_SECRET", ""),
            access_token=getenv("ACCESS_TOKEN", ""),
            adaccount_id=getenv("ADACCOUNT_ID", ""),
            form_ids=getenv("FORM_IDS", "").split(","),
        ),
        script=Script(debug=(getenv("DEBUG", "False") == "True")),
        keycrm=KeyCRM(api_token=getenv("KEYCRM_API_TOKEN", "")),
    )
