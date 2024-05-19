from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, validator
from pydantic_yaml import YamlModel
from app.core.config import settings

CONFIG_FILE_NAME = "config_test.yaml" if settings.TESTING else "config.yaml"


class AWSAccount(BaseModel):
    access_key: str
    secret_key: str
    role_arn: str


class AWSConnectionList(BaseModel):
    accounts: List[AWSAccount]

    @validator("accounts", pre=True)
    def no_duplicate_connections(cls, account_list: List[dict]) -> List[dict]:
        seen_before = []
        for account in account_list:
            cloud_id, region = account.get("cloud_id"), account.get("region")
            if f"{cloud_id}_{region}" in seen_before:
                raise ValueError(
                    f"AWS connection accounts for {cloud_id=} and {region=} appear twice, please remove one of them"
                )
            seen_before.append(f"{cloud_id}_{region}")
        return account_list

    def fetch_account(self, cloud_id: str, region: str) -> Optional[AWSAccount]:
        for account in self.accounts:
            if account.cloud_id == cloud_id and account.region == region:
                return account
        return None


class AWSConnectionSettings(BaseModel):
    aws: AWSConnectionList


class Configuration(YamlModel):
    connections: AWSConnectionSettings


configuration = Configuration.parse_file(
    path=Path(__file__).parents[3] / CONFIG_FILE_NAME, content_type="application/yaml"
)
