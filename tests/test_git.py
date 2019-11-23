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
        for message in messages:
            g.git(f"commit --allow-empty --message='{message}'")
        l = g.log()
        message_rl = list(messages)
        message_rl.reverse()
        for i in range(len(messages)):
            assert message_rl[i] == l[i]["message"]


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


@pytest.mark.parametrize(
    "message,tag",
    [
        ("feat: initial commit", "1.0.0"),
        ("test: test", "test-tag"),
        ("fix: something broken", "hello"),
    ],
)
def test_tagging(message, tag):
    with GitRepo() as g:
        g.commit(message, allow_empty=True)
        g.tag(tag)
        l = g.log()[0]
        assert l["message"] == message and l["tag"] == tag
