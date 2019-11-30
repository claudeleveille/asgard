import os
from tempfile import TemporaryDirectory

import pytest

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
        for m in messages:
            g.commit(m, allow_empty=True)
        log = g.log()
        for i in range(len(messages)):
            assert messages[i] == log[i]["message"]


@pytest.mark.parametrize(
    "message",
    [
        "feat: thing\nBREAKING CHANGE: hello",
        "test: test",
        "chore: somthing\nsomething else\n\nyet another thing",
    ],
)
def test_commiting(message):
    with GitRepo() as g:
        g.commit(message, allow_empty=True)
        assert g.log()[0]["message"] == message


@pytest.mark.parametrize(
    "message",
    [
        "feat: thing\nBREAKING CHANGE: hello",
        "test: test",
        "chore: somthing\nsomething else\n\nyet another thing",
    ],
)
def test_commiting_files(message):
    with GitRepo() as g:
        with open(g.repo_path + "/test", "w") as f:
            f.write("")
        g.add()
        g.commit(message)
        assert g.log()[0]["message"] == message


def test_tagging():
    with GitRepo() as g:
        g.commit("test: test", allow_empty=True)
        g.commit("test: test2", allow_empty=True)
        g.commit("test: test3", allow_empty=True)
        g.tag("1.0.0")
        log = g.log()[2]
        assert log["message"] == "test: test3" and log["tag"] == "1.0.0"
        g.commit("test: test4", allow_empty=True)
        log = g.log()[3]
        assert log["message"] == "test: test4" and "tag" not in log.keys()
