from pathlib import Path
import yaml


def load_config(path: str) -> dict:
    cfg = Path(path)
    if not cfg.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    with cfg.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
