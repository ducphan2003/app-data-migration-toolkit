from dynaconf import Dynaconf
from typing import Optional
import json
from urllib.parse import quote_plus
from app.utils import const

class Config:
    def __init__(self):
        self.settings = Dynaconf(
            envvar_prefix='MIGRATE',
            load_dotenv=True,
        )

        self.POSTGRES__DB: Optional[str]    = self.settings.POSTGRES__DB
        self.POSTGRES__HOST: Optional[str]  = self.settings.POSTGRES__HOST
        self.POSTGRES__PASS: Optional[str]  = quote_plus(self.settings.POSTGRES__PASS)
        self.POSTGRES__USER: Optional[str]  = quote_plus(self.settings.POSTGRES__USER)

        self.JWT_SECRET_KEY: str = self.settings.JWT_SECRET_KEY

        self.REDIS__HOST: Optional[str] = self.settings.REDIS__HOST
        self.REDIS__PORT: Optional[int] = self.settings.REDIS__PORT
        self.REDIS__DB: Optional[int]   = self.settings.REDIS__DB

        self.DIGITAL_OCEAN__STORAGE_ACCESS_KEY: Optional[str]      = self.settings.DIGITAL_OCEAN__STORAGE_ACCESS_KEY
        self.DIGITAL_OCEAN__STORAGE_SECRET_KEY: Optional[str]      = self.settings.DIGITAL_OCEAN__STORAGE_SECRET_KEY
        self.DIGITAL_OCEAN__STORAGE_REGION: Optional[str]          = self.settings.DIGITAL_OCEAN__STORAGE_REGION
        self.DIGITAL_OCEAN__STORAGE_BUCKET: Optional[str]          = self.settings.DIGITAL_OCEAN__STORAGE_BUCKET
        self.DIGITAL_OCEAN__STORAGE_ENDPOINT: Optional[str]        = self.settings.DIGITAL_OCEAN__STORAGE_ENDPOINT
        self.DIGITAL_OCEAN__IMGKIT_OUTPUT_ENDPOINT: Optional[str]  = self.settings.DIGITAL_OCEAN__IMGKIT_OUTPUT_ENDPOINT
        self.DIGITAL_OCEAN__STORAGE_ACL: Optional[str]             = self.settings.DIGITAL_OCEAN__STORAGE_ACL
        self.DIGITAL_OCEAN_DO_STORAGE_UNIVERSAL: Optional[str]     = self.settings.DIGITAL_OCEAN_DO_STORAGE_UNIVERSAL

        self.CMS_ENDPOINT        = self.settings.CMS_ENDPOINT
        self.CMS_TOKEN           = self.settings.CMS_TOKEN


app_config = Config()
