import pytest

from asgard.git import GitRepo
from asgard.semver import SemVer
from asgard.app import main, parse_args, infer_vnext, get_latest_tag_index


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


@pytest.mark.parametrize(
    "suffix,suffix_dot_suffix,suffix_dash_prefix,semver",
    [
        (None, False, False, SemVer(0, 1, 0)),
        ("rc", False, False, SemVer(0, 1, 0, suffix="rc", suffix_number=1)),
        (
            "rc",
            False,
            True,
            SemVer(0, 1, 0, suffix="rc", suffix_number=1, suffix_dash_prefix=True),
        ),
        (
            "rc",
            True,
            True,
            SemVer(
                0,
                1,
                0,
                suffix="rc",
                suffix_number=1,
                suffix_dash_prefix=True,
                suffix_dot_suffix=True,
            ),
        ),
    ],
)
def test_infers_first_version(suffix, suffix_dot_suffix, suffix_dash_prefix, semver):
    with GitRepo() as g:
        g.commit("test: test", allow_empty=True)
        g.commit("feat: test2", allow_empty=True)
        g.commit("feat: test3\nBREAKING CHANGE: test", allow_empty=True)
        assert (
            infer_vnext(
                g.log(),
                suffix=suffix,
                suffix_dot_suffix=suffix_dot_suffix,
                suffix_dash_prefix=suffix_dash_prefix,
            )
            == semver
        )


def test_infers_major_bump_correctly():
    with GitRepo() as g:
        g.commit("feat: initial commit", allow_empty=True)
        g.tag("1.1.0")
        g.commit("feat: breaking\nBREAKING CHANGE: breaking", allow_empty=True)
        assert infer_vnext(
            g.log(), suffix=None, suffix_dot_suffix=False, suffix_dash_prefix=False
        ) == SemVer(2, 0, 0)
        g.commit("feat: test\nBREAKING CHANGE: test", allow_empty=True)
        g.tag("2.0.0")
        assert infer_vnext(
            g.log(), suffix=None, suffix_dot_suffix=False, suffix_dash_prefix=False
        ) == SemVer(3, 0, 0)


def test_get_latest_tag_index():
    with GitRepo() as g:
        g.commit("test: test", allow_empty=True)
        g.commit("test: test2", allow_empty=True)
        g.tag("1.0.0")
        assert get_latest_tag_index(g.log()) == 1
