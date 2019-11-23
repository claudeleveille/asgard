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

    def add(self, path="."):
        self.git(f"add {path}")

    def commit(self, message, allow_empty=False):
        commit_opts = ""
        if allow_empty:
            commit_opts += "--allow-empty"
        self.git(f"commit {commit_opts} --file=-", stdin_str=message.encode())

    def tag(self, tag):
        self.git(f"tag {tag}")

    def log(self):
        res = self.git("log --pretty='%H'").stdout.decode().strip()
        if res:
            log = []
            for commit_hash in res.split("\n"):
                commit_dict = {
                    "hash": commit_hash,
                    "message": self.git(f"show --no-patch --format='%B' {commit_hash}")
                    .stdout.decode()
                    .strip(),
                }
                commit_describe = self.git(
                    f"describe --tags --exact-match {commit_hash}"
                )
                if commit_describe.returncode == 0:
                    commit_dict["tag"] = commit_describe.stdout.decode().strip()
                log.append(commit_dict)
            log.reverse()
            return tuple(log)
        else:
            return ()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.repo_path)
