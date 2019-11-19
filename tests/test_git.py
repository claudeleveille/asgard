import os
from tempfile import TemporaryDirectory

from asgard.git import GitRepo


def test_gitrepo_as_context_manager_leaves_no_residue():
    with GitRepo() as g:
        r = g.repo_path
        assert os.path.exists(r)
    assert not os.path.exists(r)


def test_gitrepo_is_actually_a_git_repo():
    with GitRepo() as g:
        assert g.git("status").returncode == 0


def test_gitrepo_custom_path():
    with TemporaryDirectory() as t:
        g = GitRepo(t)
        assert g.git("status").returncode == 0


def test_log_on_empty_repo():
    with GitRepo() as g:
        g.log() == ()


def test_log_with_some_commits():
    messages = ("test: test1", "test: test2", "test: test3")
    with GitRepo() as g:
        for message in messages:
            g.git(f"commit --allow-empty --message='{message}'")
        l = g.log()
        message_rl = list(messages)
        message_rl.reverse()
        for i in range(len(messages)):
            assert message_rl[i] == l[i]["message"]
