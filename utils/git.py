# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from database.types import db

import requests
import git
import os

version = (1, 0, 3)

try:
    repo = git.Repo(os.path.dirname(os.path.abspath(__name__)))
    origin = repo.remote("origin")

    repo_initialized = True

except git.exc.InvalidGitRepositoryError:
    repo = git.Repo.init(os.path.dirname(os.path.abspath(__name__)))
    origin = repo.create_remote("origin", db.get("core", "update"))

    repo_initialized = False


def check_update() -> bool:
    """
    Get updates from github repository.

    Returns:
        bool: check diff
    """
    diff = repo.git.log(
        [f"HEAD..origin/{repo.active_branch.name}", "--oneline"])

    return True if diff else False


def get_files(user, repo, path, prefix=""):
    """
    Recursively fetch files and directories from a GitHub repository.

    Args:
        user (str): The username of the repository owner.
        repo (str): The name of the repository.
        path (str): The path to the directory in the repository.
        prefix (str): The prefix to add to file names (default: "").

    Returns:
        list: A list of file and directory names.
    """

    url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"
    files = []

    response = requests.get(url)
    response.raise_for_status()

    for item in response.json():
        if item["type"] == "dir":
            dir_url = item["url"]
            dir_files = get_files(
                user, repo, item["path"], prefix + item["name"] + "/")
            files.extend(dir_files)
        else:
            files.append(prefix + item["name"])

    return files
