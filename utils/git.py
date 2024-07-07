from database.db import Database
import git
import os

version = (1, 0, 1)

db = Database("./database/data.json")
try:
    repo = git.Repo(os.path.dirname(os.path.abspath(__name__)))
    origin = repo.remote("origin")
except git.exc.InvalidGitRepositoryError:
   repo = git.Repo.init(os.path.dirname(os.path.abspath(__name__)))
   origin = repo.create_remote("origin", db.get("core", "update"))