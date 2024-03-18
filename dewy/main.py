from typing import Optional

import click

from .migration import migrate
from .serve import serve


@click.group(context_settings={"show_default": True, "max_content_width": 160})
@click.option(
    "--db",
    envvar="DB",
    show_envvar=True,
    help=("The Postgres database to connect to. " "If not provided, CRUD methods will not work."),
)
@click.pass_context
def dewy(ctx, db: Optional[str] = None):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    ctx.obj["db"] = db


dewy.add_command(serve)
dewy.add_command(migrate)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    dewy()