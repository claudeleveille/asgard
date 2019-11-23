import pytest

from asgard.git import GitRepo
from asgard.semver import SemVer
from asgard.app import main, parse_args, infer_vnext, any_tags


@pytest.mark.parametrize(
    "flag",
    ["--tag", "--commit", "--suffix-dot-suffix", "--suffix-dash-prefix", "--version"],
)
def test_flags(flag):
    attr = flag.replace("--", "").replace("-", "_")
    a = parse_args([flag])
    a_defaults = parse_args([])
    assert vars(a)[attr] == True and vars(a_defaults)[attr] == False


@pytest.mark.parametrize(
    "args,value",
    [
        ([], ""),
        (["--prerelease-suffix=hello"], "hello"),
        (["--prerelease-suffix", "hello"], "hello"),
    ],
)
def test_setting_prelease_suffix(args, value):
    a = parse_args(args)
    assert a.prerelease_suffix == value


@pytest.mark.parametrize(
    "args",
    [
        ["--version"],
        ["--version", "--commit"],
        ["--tag", "--version", "--commit"],
        ["--suffix-dot-suffix", "--version"],
    ],
)
def test_passing_version_flag_prints_version_and_exits(args, capsys):
    with pytest.raises(SystemExit):
        main(args)
    c = capsys.readouterr()
    assert SemVer.isvalid(c.out)


@pytest.mark.parametrize(
    "args",
    [
        ["--help"],
        ["-h"],
        ["-h", "--version"],
        ["--help", "--version"],
        ["--help", "--commit", "--tag"],
    ],
)
def test_passing_help_flag_shows_usage(args, capsys):
    with pytest.raises(SystemExit):
        main(args)
    c = capsys.readouterr()
    assert "usage: " in c.out


def test_any_tags_without_tags():
    with GitRepo() as g:
        assert any_tags(g.log()) == False


def test_any_tags_with_tags():
    with GitRepo() as g:
        g.commit("test", allow_empty=True)
        g.tag("test")
        assert any_tags(g.log()) == True


def test_infers_first_version():
    with GitRepo() as g:
        g.commit("test: test", allow_empty=True)
        g.commit("feat: test2", allow_empty=True)
        g.commit("feat: test3\nBREAKING CHANGE: test", allow_empty=True)
        l = g.log()
    assert infer_vnext(l) == "0.1.0"
