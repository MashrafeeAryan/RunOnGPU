from pathlib import Path

from runongpu.config import create_runongpu_template_file


def test_create_runongpu_template_file(tmp_path, monkeypatch):
    # Run the test inside a temporary folder so we do not touch the real repo.
    monkeypatch.chdir(tmp_path)

    create_runongpu_template_file()

    template_file = Path("runongpu.txt")

    assert template_file.exists()

    contents = template_file.read_text(encoding="utf-8")

    # The generated template should include all sections the parser understands.
    assert "[setup]" in contents
    assert "[build]" in contents
    assert "[test]" in contents
    assert "[run]" in contents


def test_create_runongpu_template_file_does_not_overwrite_existing_file(tmp_path, monkeypatch):
    # Existing user configs should be preserved instead of overwritten.
    monkeypatch.chdir(tmp_path)

    template_file = Path("runongpu.txt")
    template_file.write_text("[run]\npython main.py\n", encoding="utf-8")

    create_runongpu_template_file()

    assert template_file.read_text(encoding="utf-8") == "[run]\npython main.py\n"