"""clicker"""

__version__ = "0.2.5"

import click


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    click.echo(debug)
    ctx.ensure_object(dict)

    ctx.obj["DEBUG"] = debug
    # ctx.obj = Repo("fuck")
    ctx.me = "me"


class Repo:
    def __init__(self, name="none"):
        self.name = name


pass_repo = click.make_pass_decorator(Repo, ensure=True)


@cli.command()
# @click.pass_obj
@pass_repo
def status(obj):
    # click.echo(f"clicker status {ctx.obj['DEBUG']}")
    click.echo(obj.name)
    # obj["DEBUG"] = "123"
    # ctx.me = "123"
    # click.echo(ctx.parent.me)


@cli.group()
def sub():
    """
    sub command
    """
    pass


@sub.command()
def initdb():
    click.echo("Initialized the database")


@sub.command()
def dropdb():
    click.echo("Dropped the database")


main = cli
