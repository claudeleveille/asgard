import pytest

from asgard.conventionalcommits import ConventionalCommitMsg


def test_repr_is_the_full_commit_message():
    assert repr(ConventionalCommitMsg("test: test")) == "test: test"


@pytest.mark.parametrize(
    "msg",
    [
        "",
        ":",
        "FEAT: a",
        "FIX: a",
        "A: a",
        "8: a",
        " ",
        "\t",
        "\n",
        "_: a",
        "feat:a",
        "fix:a",
        "BREAKING CHANGE: a",
    ],
)
def test_badly_formatted_messages_raise_valueerror(msg):
    with pytest.raises(ValueError):
        ConventionalCommitMsg(msg)


@pytest.mark.parametrize(
    "msg,msg_type",
    [
        ("feat: a", "feat"),
        ("fix: s", "fix"),
        ("test: a", "test"),
        ("test: a", "test"),
        ("chore: a", "chore"),
        ("docs: a real test :", "docs"),
        ("perf: let's s: do this", "perf"),
        ("feat: breaking\nBREAKING CHANGE: breaks", "BREAKING CHANGE"),
    ],
)
def test_type_parsing(msg, msg_type):
    assert ConventionalCommitMsg(msg).msg_type == msg_type


def test_equality():
    msg = "feat: test"
    assert ConventionalCommitMsg(msg) == ConventionalCommitMsg(msg) == msg
