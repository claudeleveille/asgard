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
    assert vars(a)[attr] is True and vars(a_defaults)[attr] is False


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
        (None, False, False, "0.1.0"),
        ("rc", False, False, "0.1.0rc1"),
        ("rc", False, True, "0.1.0-rc1"),
        ("rc", True, True, "0.1.0-rc.1"),
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
        assert infer_vnext(g.log()) == SemVer(2, 0, 0)
        g.tag("2.0.0")
        g.commit("feat: test\nBREAKING CHANGE: test", allow_empty=True)
        assert infer_vnext(g.log()) == SemVer(3, 0, 0)


def test_infers_minor_bump_correctly():
    with GitRepo() as g:
        g.commit("chore: initial commit", allow_empty=True)
        g.tag("0.1.0")
        g.commit("feat: test", allow_empty=True)
        assert infer_vnext(g.log()) == SemVer(0, 2, 0)


def test_infers_micro_bump_correctly():
    with GitRepo() as g:
        g.commit("feat: initial commit", allow_empty=True)
        g.tag("0.1.0")
        assert infer_vnext(g.log()) == SemVer(0, 1, 1)
        g.commit("chore: test", allow_empty=True)
        g.tag("0.1.1")
        g.commit("fix: test", allow_empty=True)
        assert infer_vnext(g.log()) == SemVer(0, 1, 2)


def test_get_latest_tag_index():
    with GitRepo() as g:
        g.commit("test: test", allow_empty=True)
        g.commit("test: test2", allow_empty=True)
        assert get_latest_tag_index(g.log()) is None
        g.tag("1.0.0")
        assert get_latest_tag_index(g.log()) == 1


def test_inference_with_suffixes():
    with GitRepo() as g:
        g.commit("feat: initial commit", allow_empty=True)
        g.tag("0.1.0rc1")
        g.commit("fix: test", allow_empty=True)
        assert infer_vnext(g.log(), suffix="rc") == "0.1.0rc2"
        g.tag("0.1.0rc2")
        assert infer_vnext(g.log(), suffix="rc") == "0.1.0rc3"


def test_main_with_empty_repo():
    with GitRepo() as g:
        with pytest.raises(ValueError):
            main(["--repo-path", g.repo_path])


def test_main_first_version(capsys):
    with GitRepo() as g:
        g.commit("feat: initial commit", allow_empty=True)
        main(["--repo-path", g.repo_path])
    c = capsys.readouterr()
    assert c.out == "0.1.0\n"


def test_main_first_version_with_suffix(capsys):
    with GitRepo() as g:
        g.commit("feat: initial commit", allow_empty=True)
        main(["--repo-path", g.repo_path, "--prerelease-suffix", "rc"])
    c = capsys.readouterr()
    assert c.out == "0.1.0rc1\n"


def test_main_release_commit_and_tag(capsys):
    with GitRepo() as g:
        g.commit("feat: initial commit", allow_empty=True)
        main(["--repo-path", g.repo_path, "--commit", "--tag"])
        c = capsys.readouterr()
        assert c.out == "0.1.0\n"
        assert g.log()[1]["message"] == "release: 0.1.0"
        assert g.log()[1]["tag"] == "v0.1.0"


def test_main_release_tag_no_commit(capsys):
    with GitRepo() as g:
        g.commit("feat: initial commit", allow_empty=True)
        main(["--repo-path", g.repo_path, "--tag"])
        c = capsys.readouterr()
        assert c.out == "0.1.0\n"
        assert g.log()[0]["message"] == "feat: initial commit"
        assert g.log()[0]["tag"] == "v0.1.0"


def test_version_inference_with_default_v_prefix():
    with GitRepo() as g:
        g.commit("feat: test", allow_empty=True)
        main(["--repo-path", g.repo_path, "--tag"])
        g.commit("fix: test", allow_empty=True)
        assert infer_vnext(g.log()) == "0.1.1"


def test_version_inference_with_non_cc_commit_msg():
    with GitRepo() as g:
        g.commit("test", allow_empty=True)
        g.tag("v0.1.0")
        g.commit("test2", allow_empty=True)
        assert infer_vnext(g.log()) == "0.1.1"
