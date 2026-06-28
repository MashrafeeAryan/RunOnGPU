import runongpu.config as config_module


def test_save_and_load_repo_config(tmp_path, monkeypatch):
    # Store config in a temp folder so this test never touches the user's real ~/.runongpu.
    fake_config_dir = tmp_path / ".runongpu"
    fake_config_file = fake_config_dir / "config.json"

    monkeypatch.setattr(config_module, "CONFIG_DIR", fake_config_dir)
    monkeypatch.setattr(config_module, "CONFIG_FILE", fake_config_file)

    config_module.save_repo_url(
        "https://github.com/MashrafeeAryan/RunOnGPU.git",
        "RunOnGPU",
    )

    result = config_module.load_config()

    assert result["repo_url"] == "https://github.com/MashrafeeAryan/RunOnGPU.git"
    assert result["folder_name"] == "RunOnGPU"
    assert result["notebook_url"] == ""


def test_save_notebook_url_updates_existing_config(tmp_path, monkeypatch):
    # Notebook URL should be saved so future runs reuse the same Colab notebook.
    fake_config_dir = tmp_path / ".runongpu"
    fake_config_file = fake_config_dir / "config.json"

    monkeypatch.setattr(config_module, "CONFIG_DIR", fake_config_dir)
    monkeypatch.setattr(config_module, "CONFIG_FILE", fake_config_file)

    config_module.save_repo_url(
        "https://github.com/MashrafeeAryan/RunOnGPU.git",
        "RunOnGPU",
    )

    config_module.save_notebook_url("https://colab.research.google.com/drive/test")

    result = config_module.load_config()

    assert result["repo_url"] == "https://github.com/MashrafeeAryan/RunOnGPU.git"
    assert result["folder_name"] == "RunOnGPU"
    assert result["notebook_url"] == "https://colab.research.google.com/drive/test"