from functools import partial

from invoke import task, run


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
def build(c):
    sh("pyinstaller asgard.spec")


@task
def clean(c):
    sh("git clean -dfx")
