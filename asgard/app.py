import argparse
import os
import sys

from asgard._version import __version__
from asgard.git import GitRepo
from asgard.semver import SemVer
from asgard.conventionalcommits import ConventionalCommitMsg


def main(args=sys.argv[1:]):
    a = parse_args(args)

    if a.version:
        print(__version__)
        sys.exit(0)

    g = GitRepo(a.repo_path)

    if len(g.log()) == 0:
        raise ValueError(f"No commits found in git repo at {a.repo_path}.")

    vnext = infer_vnext(
        g.log(),
        suffix=a.prerelease_suffix,
        suffix_dash_prefix=a.suffix_dash_prefix,
        suffix_dot_suffix=a.suffix_dot_suffix,
    )
    print(vnext)
    if a.commit:
        g.commit(f"release: {vnext}", allow_empty=True)
    if a.tag:
        g.tag(f"v{vnext}")


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument("--commit", action="store_true", default=False)
    parser.add_argument("--tag", action="store_true", default=False)
    parser.add_argument("--suffix-dot-suffix", action="store_true", default=False)
    parser.add_argument("--suffix-dash-prefix", action="store_true", default=False)
    parser.add_argument("--version", action="store_true", default=False)
    parser.add_argument("--prerelease-suffix", default="")
    parser.add_argument("--repo-path", default=os.getcwd())

    return parser.parse_args(args)


def get_latest_tag_index(log):
    latest = None
    for i in range(len(log)):
        if "tag" in log[i].keys():
            latest = i
    return latest


def infer_vnext(log, suffix=None, suffix_dot_suffix=False, suffix_dash_prefix=False):
    latest_tag_index = get_latest_tag_index(log)
    if latest_tag_index == None:
        if suffix:
            return SemVer(
                0,
                1,
                0,
                suffix=suffix,
                suffix_number=1,
                suffix_dot_suffix=suffix_dot_suffix,
                suffix_dash_prefix=suffix_dash_prefix,
            )
        else:
            return SemVer(0, 1, 0)
    else:
        version = SemVer.fromstr(log[latest_tag_index]["tag"].replace("v", ""))
        if (
            version.isprerelease()
            and version.suffix_dash_prefix == suffix_dash_prefix
            and version.suffix == suffix
            and version.suffix_dot_suffix == suffix_dot_suffix
        ):
            version.increment_suffix_number()
            return version
        if latest_tag_index == len(log) - 1:
            version.increment_micro()
            return version
        major_bump, minor_bump = False, False
        for commit in log[latest_tag_index + 1 :]:
            cc_msg_type = ConventionalCommitMsg(commit["message"]).msg_type
            if cc_msg_type == "BREAKING CHANGE":
                major_bump = True
            elif cc_msg_type == "feat":
                minor_bump = True
        if major_bump:
            version.increment_major()
        elif minor_bump:
            version.increment_minor()
        else:
            version.increment_micro()
        return version
