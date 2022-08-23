# -*- coding: utf-8 -*-
"""CLI main entrypoint."""

import os

import click
from loguru import logger

from ghpm.util import (
    common_params,
    create_discussion,
    create_todo,
    GHPM_DOC_CAT,
    GHPM_NOTE_CAT,
    GHPM_OPEN_URL,
    GHPM_PAT,
    GHPM_REPO_NAME,
    GHPM_REPO_OWNER,
    GHPM_REPO_URL,
    make_request,
)


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli() -> None:
    """Project management through Github issues and discussions.

    Manage your work through one of the following objects:

    \b
    * TODO - a work item that needs to be done; implemented as a Github Issue which is closeable
    * NOTE - a quick, short, note; implemented as a Github Discussion, categorized as "Ideas"
    * DOC  - a deliberate, thoughtout document (cleaner than a NOTE); implemented as a Github
             Discussion, categorized as "General"

    \b
    Examples
    --------

    \b
    Confirm CLI is setup and can communicate with Github
    >>> ghpm debug

    \b
    Create a TODO (Github issues) with the title 'todo title' & again with a body
    >>> ghpm todo 'todo title'
    >>> ghpm todo 'todo title' -b 'body of the todo'

    \b
    Create a note (Github discussion) with the title 'note title' & again with a body
    >>> ghpm note 'note title'
    >>> ghpm note 'note title' -b 'body of the note'

    \b
    Open the targer repository in a browser.
    >>> ghpm open
    """


@click.command()
def debug() -> None:
    """Check the connection to Github."""
    headers = {"Accept": "application/vnd.github+json"}
    make_request(GHPM_REPO_URL, headers, ("token", GHPM_PAT), "get")
    logger.info(f"{GHPM_REPO_OWNER=}")
    logger.info(f"{GHPM_REPO_NAME=}")
    logger.info(f"{GHPM_DOC_CAT=}")
    logger.info(f"{GHPM_NOTE_CAT=}")
    logger.info(f"{GHPM_OPEN_URL=}")
    logger.info("Setup successful!")


@click.command()
@common_params
def todo(title: str, open_obj: bool, body: str) -> None:
    """Create a TODO.

    \b
    Examples
    --------
    Create a TODO (Github issues) with the title 'todo title' & again with a body
    >>> ghpm todo 'todo title'
    >>> ghpm todo 'todo title' -b 'body of the todo'
    """
    create_todo(title=title, open_obj=open_obj, body=body)


@click.command()
@common_params
def doc(title: str, open_obj: bool, body: str) -> None:
    """Create a DOC.

    \b
    Examples
    --------
    Create a doc (Github discussion) with the title 'doc title' & again with a body
    >>> ghpm doc 'doc title'
    >>> ghpm doc 'doc title' -b 'body of the doc'
    """
    create_discussion(title=title, open_obj=open_obj, category_name=GHPM_DOC_CAT)


@click.command()
@common_params
def note(title: str, open_obj: bool, body: str) -> None:
    """Create a NOTE.

    \b
    Examples
    --------
    Create a note (Github discussion) with the title 'note title' & again with a body
    >>> ghpm note 'note title'
    >>> ghpm note 'note title' -b 'body of the note'
    """
    create_discussion(title=title, open_obj=open_obj, category_name=GHPM_NOTE_CAT)


@click.command()
def open() -> None:
    """Open the target respository in browser."""
    os.system(f"open {GHPM_OPEN_URL}")


cli.add_command(debug)
cli.add_command(doc)
cli.add_command(todo)
cli.add_command(note)
cli.add_command(open)

if __name__ == "__main__":
    cli()
