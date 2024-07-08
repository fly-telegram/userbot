from database.db import Database
import git
import os

version = (1, 0, 2)

db = Database("./database/data.json")
try:
    repo = git.Repo(os.path.dirname(os.path.abspath(__name__)))
    origin = repo.remote("origin")

    repo_initialized = True

except git.exc.InvalidGitRepositoryError:
    repo = git.Repo.init(os.path.dirname(os.path.abspath(__name__)))
    origin = repo.create_remote("origin", db.get("core", "update"))

    repo_initialized = False


def check_update() -> bool:
    diff = repo.git.log(
        [
            f"HEAD..origin/{repo.active_branch.name}",
            "--oneline"
        ]
    )

    return True if diff else False
