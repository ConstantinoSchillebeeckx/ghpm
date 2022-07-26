# -*- coding: utf-8 -*-
"""Github Project Management.

https://github.com/ConstantinoSchillebeeckx/todo
https://docs.github.com/en/rest/issues/issues#create-an-issue
https://docs.github.com/en/graphql/reference/objects#discussion
https://docs.github.com/en/graphql/guides/using-the-graphql-api-for-discussions

todo - issue
doc - discussion general
note - discussion idea
"""

import os

import click
import requests
from loguru import logger

from ghpm.util import (
    common_params,
    create_discussion,
    DOC_DISCUSSION_CATEGORY,
    make_request,
    NOTE_DISCUSSION_CATEGORY,
    OPEN_URL,
    REPO_NAME,
    REPO_OWNER,
    REPO_URL,
    TOKEN,
)


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli() -> None:
    """Project management and TODOs with Github issues and discussions.

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
    """


@click.command()
def debug() -> None:
    """Check the connection to Github."""
    headers = {"Accept": "application/vnd.github+json"}
    make_request(REPO_URL, headers, ("token", TOKEN), "get")
    logger.info(f"Setup successful for {REPO_OWNER=} in {REPO_NAME=}")


@click.command()
@common_params
def todo(title: str, open_obj: bool, body: str) -> None:
    """Create a TODO as a Github issue.

    \b
    Examples
    --------
    >>> ghpm todo 'some title'
    """
    payload = {"title": title, "labels": ["todo"], "body": body}
    headers = {
        "Accept": "application/vnd.github+json",
    }
    r = requests.post(f"{REPO_URL}/issues", json=payload, headers=headers, auth=("token", TOKEN))
    d = r.json()
    logger.info(f"Created issue {d['html_url']}")

    if open_obj:
        os.system(f"open {d['html_url']}")


@click.command()
@common_params
def doc(title: str, open_obj: bool, body: str) -> None:
    """Create a doc as Github discussion, categorized as "General"."""
    create_discussion(title=title, open_obj=open_obj, category_name=DOC_DISCUSSION_CATEGORY)


@click.command()
@common_params
def note(title: str, open_obj: bool, body: str) -> None:
    """Create a note as Github discussion, categorized as "Ideas"."""
    create_discussion(title=title, open_obj=open_obj, category_name=NOTE_DISCUSSION_CATEGORY)


@click.command()
def open() -> None:
    """Open target respository in browser."""
    os.system(f"open {OPEN_URL}")


cli.add_command(debug)
cli.add_command(doc)
cli.add_command(todo)
cli.add_command(note)
cli.add_command(open)

if __name__ == "__main__":
    cli()
