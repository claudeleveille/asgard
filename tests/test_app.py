import pytest

from asgard.semver import SemVer
from asgard.app import main, parse_args


@pytest.mark.parametrize(
    "flag",
    ["--tag", "--commit", "--suffix-dot-suffix", "--suffix-dash-prefix", "--version"],
)
def test_flags(flag):
    attr = flag.replace("--", "").replace("-", "_")
    a = parse_args([flag])
    a_defaults = parse_args([])
    assert vars(a)[attr] == True and vars(a_defaults)[attr] == False


def test_default_prerelease_suffix():
    a = parse_args([])
    assert a.prerelease_suffix == ""


@pytest.mark.parametrize(
    "args,value",
    [
        (["--prerelease-suffix=hello"], "hello"),
        (["--prerelease-suffix", "hello"], "hello"),
    ],
)
def test_setting_prelease_suffix(args, value):
    a = parse_args(args)
    assert a.prerelease_suffix == value


def test_passing_version_flag_prints_version_and_exits(capsys):
    with pytest.raises(SystemExit):
        main(["--version"])
    c = capsys.readouterr()
    assert SemVer.isvalid(c.out)
