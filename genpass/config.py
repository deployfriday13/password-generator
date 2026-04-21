import os
import sys
import tomllib
from pathlib import Path


DEFAULTS: dict = {
    "password": {
        "length": 15,
        "uppercase": True,
        "lowercase": True,
        "digits": True,
        "symbols": True,
    },
    "phrase": {
        "length": 6,
        "delimiter": "-",
    },
}


def config_path() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path.home() / ".config"
    return base / "genpass" / "config.toml"


def load_config() -> dict:
    path = config_path()
    if not path.exists():
        return DEFAULTS

    with open(path, "rb") as f:
        data = tomllib.load(f)

    return {
        "password": {**DEFAULTS["password"], **data.get("password", {})},
        "phrase": {**DEFAULTS["phrase"], **data.get("phrase", {})},
    }


def save_config(config: dict) -> None:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    p = config["password"]
    ph = config["phrase"]

    toml = (
        "[password]\n"
        f"length = {p['length']}\n"
        f"uppercase = {str(p['uppercase']).lower()}\n"
        f"lowercase = {str(p['lowercase']).lower()}\n"
        f"digits = {str(p['digits']).lower()}\n"
        f"symbols = {str(p['symbols']).lower()}\n"
        "\n"
        "[phrase]\n"
        f"length = {ph['length']}\n"
        f'delimiter = "{ph["delimiter"]}"\n'
    )

    path.write_text(toml)
