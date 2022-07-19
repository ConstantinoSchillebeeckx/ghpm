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

import functools
import os
import sys
from typing import Any, Callable

import click
import requests
import util
from loguru import logger
from util import REPO_NAME, REPO_OWNER, REPO_URL, TOKEN

logger.remove()
fmt = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <lvl>{message}</lvl>"
)
logger.add(sys.stderr, format=fmt)


def common_params(func: Callable) -> Callable:
    """Get common options/arguments for shared among all commands."""

    @click.argument("title")
    @click.option(
        "-o/-n",
        "--open/--no-open",
        "open_obj",
        default=False,
        help="Whether to open (default) or not open the created TODO",
    )
    @click.option("-b", "--body", default=None, help="Optional body text")
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Callable:
        return func(*args, **kwargs)

    return wrapper


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli() -> None:
    """Get main entrypoint."""


@click.command()
def debug() -> None:
    """Check the connection to Github."""
    headers = {"Accept": "application/vnd.github+json"}
    util.make_request(REPO_URL, headers, ("token", TOKEN), "get")
    logger.info(f"Setup successful for {REPO_OWNER=} in {REPO_NAME=}")


@click.command()
@common_params
def todo(title: str, open_obj: str, body: str) -> None:
    r"""Create a TODO as a Github issue.

    \b
    Examples
    --------
    >>> python main.py todo 'some title'
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
def note(title: str, open_obj: str) -> None:
    """Create a note as Github discussion.

    https://docs.github.com/en/graphql/reference/objects#discussion
    """
    util.create_discussion(title=title, open_obj=open_obj, category_name="general")


cli.add_command(debug)
cli.add_command(todo)
cli.add_command(note)

if __name__ == "__main__":
    cli()
