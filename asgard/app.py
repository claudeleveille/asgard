import argparse
import sys

from asgard._version import __version__
from asgard.semver import SemVer


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


def any_tags(log):
    for i in log:
        if "tag" in i.keys():
            return True
    return False


def infer_vnext(log, suffix, suffix_dot_suffix, suffix_dash_prefix):
    if not any_tags(log):
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
