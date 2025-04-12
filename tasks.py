from invoke import task


@task
def start(ctx):
    ctx.run("python3 src/index.py", pty=True)


@task
def test(ctx):
    ctx.run("pytest src", pty=True)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)


@task
def init_db(ctx):
    ctx.run("python3 src/utils/database/initialize_database.py", pty=True)


@task
def lint(ctx):
    ctx.run("pylint src", pty=True)
