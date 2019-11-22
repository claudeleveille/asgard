import subprocess
import os
import shutil
from tempfile import mkdtemp


class GitRepo:
    def __init__(self, repo_path=None):
        if repo_path is not None and os.path.exists(repo_path):
            self.repo_path = repo_path
        else:
            self.repo_path = mkdtemp()
        self.git("init")

    def git(self, cmd, stdin_str=None):
        return subprocess.run(
            f"git {cmd}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            input=stdin_str,
            cwd=self.repo_path,
        )

    def log(self):
        res = self.git("log --pretty='%H'").stdout.decode()
        if res:
            rv = []
            for commit_hash in res.split("\n"):
                rv.append(
                    {
                        "hash": commit_hash,
                        "message": self.git(
                            f"show --no-patch --format='%B' {commit_hash}"
                        )
                        .stdout.decode()
                        .strip(),
                    }
                )
            return tuple(rv)
        else:
            return ()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.repo_path)
