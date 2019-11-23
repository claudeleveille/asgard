import argparse
import sys

from asgard._version import __version__
from asgard.semver import SemVer
from asgard.conventionalcommits import ConventionalCommitMsg


def main(args=sys.argv[1:]):
    a = parse_args(args)

    if a.version:
        print(__version__)
        sys.exit(0)


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument("--commit", action="store_true", default=False)
    parser.add_argument("--tag", action="store_true", default=False)
    parser.add_argument("--suffix-dot-suffix", action="store_true", default=False)
    parser.add_argument("--suffix-dash-prefix", action="store_true", default=False)
    parser.add_argument("--version", action="store_true", default=False)
    parser.add_argument("--prerelease-suffix", default="")

    return parser.parse_args(args)


def get_latest_tag_index(log):
    latest = None
    for i in range(len(log)):
        if "tag" in log[i].keys():
            latest = i
    return latest


def infer_vnext(log, suffix, suffix_dot_suffix, suffix_dash_prefix):
    if get_latest_tag_index(log) == None:
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
        lti = get_latest_tag_index(log)
        version = SemVer.fromstr(log[lti]["tag"])
        for l in log[lti:]:
            if ConventionalCommitMsg(l["message"]).msg_type == "BREAKING CHANGE":
                version.increment_major()
                return version
