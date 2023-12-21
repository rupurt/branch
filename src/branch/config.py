import os
import yaml
from pydantic import BaseModel, Field
from typing_extensions import Any, Optional

default_config = "branch.yaml"


class ServerSettings(BaseModel):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=9000)
    ui_port: int = Field(default=8999)
    log_level: str = Field(default="info")


class StorageSettings(BaseModel):
    location: str = Field(default="local://.branch")
    create: bool = Field(default=False)


class CLITableSettings(BaseModel):
    width: Optional[int] = Field(default=None)


class CLISettings(BaseModel):
    table: CLITableSettings = CLITableSettings()


class FeatureFlagSettings(BaseModel):
    tui: bool = Field(default=False)


class Settings(BaseModel):
    server: ServerSettings = ServerSettings()
    storage: StorageSettings = StorageSettings()
    cli: CLISettings = CLISettings()
    feature_flag: FeatureFlagSettings = FeatureFlagSettings()


def read_settings(config_file_path: str) -> Settings:
    """
    Reads the branch configuration yaml file and override attributes with environment variables.

    The order of precedence is:
        1. environment variables
        2. yaml file
        3. python defined default values
    """
    yaml_config = _read_yaml_config(config_file_path)
    env_config = _read_env_config()
    config = yaml_config | env_config
    settings = Settings(**config)
    return settings


def _read_yaml_config(file_path: str) -> dict[Any, Any]:
    try:
        with open(file_path, "r") as stream:
            yaml_config = yaml.safe_load(stream) or {}
    except FileNotFoundError:
        yaml_config = {}
    return yaml_config


DEFAULT_ENV_SCHEMA = {
    "server": ["host", "port", "ui_port", "log_level"],
    "storage": ["location", "create"],
    "cli": {
        "table": ["width"],
    },
    "feature_flag": [
        "tui",
    ],
}


def _read_env_config(
    env_schema: dict[str, Any] | list[str] = DEFAULT_ENV_SCHEMA,
    parents: list[str] = ["BRANCH"],
    acc: dict[str, Any] = {},
) -> dict[str, Any]:
    if isinstance(env_schema, list):
        for attr in env_schema:
            key_segments = [*parents, attr.upper()]
            env_key = "_".join(key_segments)
            value = os.getenv(env_key)
            if value:
                acc[attr] = value
    elif isinstance(env_schema, dict):
        for attr, attr_values in env_schema.items():
            new_parents = [*parents, attr.upper()]
            value = _read_env_config(attr_values, new_parents, {})
            if value != {}:
                acc[attr] = value
    return acc
