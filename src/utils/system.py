import json
import os.path
from pathlib import Path
from typing import Any


def save_json(path: Path, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_json(path: Path) -> Any | None:
    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
