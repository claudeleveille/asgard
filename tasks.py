from functools import partial

from invoke import task, run


DOCKER_REPO = "claudeleveille/asgard"
VERSION = "0.1.0rc1"


sh = partial(run, echo=True)


@task
def fmt(c):
    sh("black --verbose .")


@task
def check(c):
    sh("black --check --verbose --diff .")
    sh("pyflakes .")


@task
def test(c):
    sh("pytest --verbose --ff --cov=asgard", pty=True)


@task
def package(c):
    sh("pyinstaller asgard.spec")
    sh(f"docker build --pull --tag {DOCKER_REPO}:{VERSION} .")


@task
def clean(c):
    sh("git clean -dfx")
