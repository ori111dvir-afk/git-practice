import json
import re
from pathlib import Path
from typing import Any, Dict


def slugify(text: str) -> str:
    """Convert text into a URL-friendly slug.

    Non-alphanumeric characters are replaced with hyphens, and the result is
    lowercased with leading/trailing hyphens stripped.
    """
    if not isinstance(text, str):
        raise TypeError("slugify() expects a string")

    normalized = text.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized)
    return slug.strip("-")


def read_json(path: str) -> Dict[str, Any]:
    """Read a JSON file and return its contents as a dictionary.

    Raises FileNotFoundError if the path does not exist, ValueError if the JSON is invalid,
    or TypeError if the file contents are not a JSON object.
    """
    file_path = Path(path)
    try:
        with file_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise TypeError(f"Expected JSON object in {path}, got {type(data).__name__}")

    return data


def write_json(path: str, data: Dict[str, Any]) -> None:
    """Write a dictionary to a JSON file with UTF-8 encoding.

    Raises TypeError if data is not a dictionary.
    """
    if not isinstance(data, dict):
        raise TypeError("write_json() expects a dictionary")

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
