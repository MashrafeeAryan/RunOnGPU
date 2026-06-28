from runongpu.config import get_folder_name_from_repo_url


def test_get_folder_name_from_https_repo_url():
    # Git clones this URL into a local folder named "RunOnGPU".
    result = get_folder_name_from_repo_url(
        "https://github.com/MashrafeeAryan/RunOnGPU.git"
    )

    assert result == "RunOnGPU"


def test_get_folder_name_from_url_without_git_suffix():
    # GitHub URLs may be copied without ".git", so both formats should work.
    result = get_folder_name_from_repo_url(
        "https://github.com/MashrafeeAryan/runongpu-examples"
    )

    assert result == "runongpu-examples"


def test_get_folder_name_from_url_with_trailing_slash():
    # Trailing slashes should not create an empty folder name.
    result = get_folder_name_from_repo_url(
        "https://github.com/MashrafeeAryan/runongpu-examples/"
    )

    assert result == "runongpu-examples"