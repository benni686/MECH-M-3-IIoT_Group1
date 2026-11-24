import sys
import tomllib
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "cloud"))

from config_loader import ConfigError, load_settings  # noqa: E402


def test_shared_settings_contain_no_passwords():
    with (ROOT / "settings.toml").open("rb") as handle:
        shared = tomllib.load(handle)
    assert "password" not in shared["broker"]["course"]
    assert "password" not in shared["grafana"]
    assert "private" not in shared["broker"]


def test_local_settings_is_ignored():
    patterns = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert "settings.local.toml" in patterns


def test_course_profile_is_merged(tmp_path):
    private = tmp_path / "settings.local.toml"
    private.write_text('[broker.course]\npassword = "secret"\n', encoding="utf-8")
    settings = load_settings(ROOT / "settings.toml", private)
    assert settings["broker"]["selected_name"] == "course"
    assert settings["broker"]["selected"]["host"] == "158.180.44.197"
    assert settings["broker"]["selected"]["password"] == "secret"


def test_missing_password_is_rejected(tmp_path):
    private = tmp_path / "settings.local.toml"
    private.write_text("[broker.course]\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="password"):
        load_settings(ROOT / "settings.toml", private)


def test_private_profile_can_override_course_profile(tmp_path):
    private = tmp_path / "settings.local.toml"
    private.write_text(
        """
[broker]
active = "private"

[broker.course]
password = "course-secret"

[broker.private]
host = "private.example.com"
port = 8883
username = "private-user"
password = "private-secret"
tls = true
""".lstrip(),
        encoding="utf-8",
    )
    settings = load_settings(ROOT / "settings.toml", private)
    assert settings["broker"]["selected_name"] == "private"
    assert settings["broker"]["selected"]["tls"] is True
