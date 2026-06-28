import pytest

from runongpu.parser import parse_config


def test_parse_valid_config(tmp_path, monkeypatch):
    config_file = tmp_path / "runongpu.txt"
    config_file.write_text(
        """
# RunOnGPU config

[setup]
pip install -r requirements.txt

[build]
nvcc main.cu -o vector_add

[test]
pytest

[run]
./vector_add
""",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    result = parse_config()

    assert result == {
        "setup": ["pip install -r requirements.txt"],
        "build": ["nvcc main.cu -o vector_add"],
        "test": ["pytest"],
        "run": ["./vector_add"],
    }


def test_parse_empty_sections(tmp_path, monkeypatch):
    config_file = tmp_path / "runongpu.txt"
    config_file.write_text(
        """
[setup]

[build]

[test]

[run]
""",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    assert parse_config() == {
        "setup": [],
        "build": [],
        "test": [],
        "run": [],
    }


def test_unknown_section_raises_error(tmp_path, monkeypatch):
    config_file = tmp_path / "runongpu.txt"
    config_file.write_text(
        """
[install]
pip install numpy
""",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    with pytest.raises(ValueError, match="Unknown section"):
        parse_config()


def test_command_before_section_raises_error(tmp_path, monkeypatch):
    config_file = tmp_path / "runongpu.txt"
    config_file.write_text(
        """
pip install numpy

[run]
python main.py
""",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    with pytest.raises(ValueError, match="Command found before any section header"):
        parse_config()