"""Prepare file-based runtime secrets for services that cannot read TOML."""

from pathlib import Path

from config_loader import ConfigError, load_settings


def main() -> None:
    settings = load_settings()
    grafana = settings.get("grafana", {})
    username = grafana.get("admin_user")
    password = grafana.get("admin_password")
    if not isinstance(username, str) or not username.strip():
        raise ConfigError("grafana.admin_user fehlt in settings.toml")
    if not isinstance(password, str) or not password.strip():
        raise ConfigError("grafana.admin_password fehlt in settings.local.toml")
    secrets = {
        "grafana_admin_user": username.strip(),
        "grafana_admin_password": password.strip(),
    }
    target_dir = Path("/run-config")
    target_dir.mkdir(parents=True, exist_ok=True)
    for name, value in secrets.items():
        target = target_dir / name
        target.write_text(value, encoding="utf-8")
        target.chmod(0o444)


if __name__ == "__main__":
    main()
