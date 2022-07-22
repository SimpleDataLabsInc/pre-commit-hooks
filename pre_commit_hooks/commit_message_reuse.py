import typer
from git import Repo
from typing import Optional
from pathlib import Path


def check_commit_messages(input_file: Path, repo_dir: Path = Path('.'),
                          log_depth: Optional[int] = 50):
    repo = Repo(repo_dir)
    input_str = open(input_file).read().strip().lower()
    for commit in list(repo.iter_commits())[:log_depth]:
        cmsg = commit.message.strip().lower()
        print(f"'{input_str}' -> '{cmsg}'")
        if cmsg.startswith(input_str):
            raise ValueError(
                f"Commit message '{input_str}' is too similar to message of"
                " commit '{commit.hexsha}': '{cmsg}'")


def main():
    return typer.run(check_commit_messages)


if __name__ == '__main__':
    raise SystemExit(main)
