from __future__ import annotations
from dulwich.repo import Repo
from dulwich.porcelain import pull, clone
from native_builder.config import ROOT

def git_dep(package_name: str, url: str, branch: str | None = None, update: bool = False):
    local_repo_dir = ROOT.joinpath("GitDependencies", package_name)
    local_repo_dir.mkdir(parents=True, exist_ok=True, mode=0o755)
    if not local_repo_dir.joinpath(".git").exists():
        repo = clone(url, local_repo_dir.as_posix(), checkout=True, branch=branch)
    else:
        repo = Repo(local_repo_dir.as_posix())
    if update:
        pull(repo, url)
    return repo
