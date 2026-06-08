import json
import importlib.util
from pathlib import Path

import pytest


def _load_utils_module():
    """Dynamically load the `src/utils.py` module for tests."""
    path = Path(__file__).parent.parent / "src" / "utils.py"
    spec = importlib.util.spec_from_file_location("utils", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_slugify_basic():
    utils = _load_utils_module()
    assert utils.slugify("Hello World!") == "hello-world"


def test_slugify_strip_and_collapse():
    utils = _load_utils_module()
    assert utils.slugify("  Multiple --- Separators  ") == "multiple-separators"


def test_slugify_type_error():
    utils = _load_utils_module()
    with pytest.raises(TypeError):
        utils.slugify(123)  # type: ignore


def test_write_and_read_json(tmp_path):
    utils = _load_utils_module()
    data = {"name": "alice", "age": 30}
    out = tmp_path / "subdir" / "data.json"
    utils.write_json(str(out), data)
    assert out.exists()
    read = utils.read_json(str(out))
    assert read == data


def test_write_json_type_error(tmp_path):
    utils = _load_utils_module()
    with pytest.raises(TypeError):
        utils.write_json(str(tmp_path / "bad.json"), [1, 2, 3])


def test_read_json_invalid_json(tmp_path):
    utils = _load_utils_module()
    p = tmp_path / "invalid.json"
    p.write_text("not a json")
    with pytest.raises(ValueError):
        utils.read_json(str(p))


def test_read_json_not_object(tmp_path):
    utils = _load_utils_module()
    p = tmp_path / "array.json"
    p.write_text(json.dumps([1, 2, 3]))
    with pytest.raises(TypeError):
        utils.read_json(str(p))


def test_read_json_file_not_found():
    utils = _load_utils_module()
    with pytest.raises(FileNotFoundError):
        utils.read_json("this_file_should_not_exist_hopefully.json")
