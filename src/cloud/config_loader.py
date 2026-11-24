"""Load and validate the shared TOML configuration."""

from __future__ import annotations

import os
import tomllib
from copy import deepcopy
from pathlib import Path
from typing import Any


class ConfigError(RuntimeError):
    """Raised when the project configuration is missing or invalid."""


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def _default_paths() -> tuple[Path, Path]:
    container_settings = Path("/config/settings.toml")
    if container_settings.is_file():
        return container_settings, Path("/config/settings.local.toml")
    root = Path(__file__).resolve().parents[2]
    return root / "settings.toml", root / "settings.local.toml"


def _read_toml(path: Path, *, required: bool) -> dict[str, Any]:
    if not path.is_file():
        if required:
            raise ConfigError(f"Konfigurationsdatei fehlt: {path}")
        return {}
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ConfigError(f"Konfiguration kann nicht gelesen werden: {path}: {error}") from error


def _required_text(section: dict[str, Any], key: str, label: str) -> str:
    value = section.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{label}.{key} fehlt oder ist leer")
    return value.strip()


def load_settings(
    settings_path: str | Path | None = None,
    local_path: str | Path | None = None,
) -> dict[str, Any]:
    default_settings, default_local = _default_paths()
    shared_path = Path(settings_path or os.getenv("IIOT_SETTINGS_FILE", default_settings))
    private_path = Path(local_path or os.getenv("IIOT_LOCAL_SETTINGS_FILE", default_local))
    settings = _merge(
        _read_toml(shared_path, required=True),
        _read_toml(private_path, required=True),
    )

    broker_root = settings.get("broker")
    if not isinstance(broker_root, dict):
        raise ConfigError("Sektion [broker] fehlt")
    profile = _required_text(broker_root, "active", "broker")
    profile_settings = broker_root.get(profile)
    if not isinstance(profile_settings, dict):
        raise ConfigError(f"Sektion [broker.{profile}] fehlt")
    _required_text(profile_settings, "host", f"broker.{profile}")
    _required_text(profile_settings, "username", f"broker.{profile}")
    _required_text(profile_settings, "password", f"broker.{profile}")
    port = profile_settings.get("port")
    if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
        raise ConfigError(f"broker.{profile}.port muss zwischen 1 und 65535 liegen")
    if not isinstance(profile_settings.get("tls"), bool):
        raise ConfigError(f"broker.{profile}.tls muss true oder false sein")

    settings["broker"]["selected"] = profile_settings
    settings["broker"]["selected_name"] = profile
    return settings
