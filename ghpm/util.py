# -*- coding: utf-8 -*-
"""Utilities."""

import functools
import os
from string import Template
from typing import Any, Callable, Dict

import click
import requests
from decouple import config
from loguru import logger

REPO_OWNER = config("REPO_OWNER")
REPO_NAME = config("REPO_NAME")
REPO = f"{REPO_OWNER}/{REPO_NAME}"
REPO_URL = f"https://api.github.com/repos/{REPO}"
TOKEN = config("TOKEN")


def common_params(func: Callable) -> Callable:
    """Get common options/arguments for shared among all commands."""

    @click.argument("title")
    @click.option(
        "-o/-n",
        "--open/--no-open",
        "open_obj",
        default=True,
        help="Whether to open (default) or not open the created Github object",
    )
    @click.option("-b", "--body", default=None, help="Optional body text")
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Callable:
        return func(*args, **kwargs)

    return wrapper


def make_request(url: str, headers: dict, auth: Any, request_type: str = "post") -> dict:
    """Make a generic request."""
    if request_type == "post":
        r = requests.post(url, headers=headers, auth=auth)
    elif request_type == "get":
        r = requests.get(url, headers=headers, auth=auth)

    r.raise_for_status()

    return r.json()


def create_discussion(title: str, open_obj: bool, category_name: str) -> None:
    """Create a discussion.

    https://docs.github.com/en/graphql/reference/objects#discussion
    """
    repo_id = get_repo_id()
    discussions = get_discussion_categories()
    category_id = discussions["general"]

    headers: Dict[str, str] = {}
    query = Template(
        """
        mutation {
            createDiscussion(input: {
                repositoryId: "$repo_id",
                categoryId: "$category_id",
                body: "The body", title: "$title"}) {
            discussion {
              id, url
            }
          }
        }
        """
    ).substitute(repo_id=repo_id, category_id=category_id, title=title)
    logger.debug(f"Creating discussion with {query}")
    r = requests.post(
        "https://api.github.com/graphql", json={"query": query}, headers=headers, auth=("token", TOKEN)
    )
    d = r.json()
    url = d["data"]["createDiscussion"]["discussion"]["url"]
    logger.info(f"Created discussion {url}")

    if open_obj:
        os.system(f"open {url}")


def get_repo_id() -> str:
    """Get the repository ID."""
    return get_repo()["data"]["repository"]["id"]


@functools.lru_cache
def get_discussion_categories() -> Dict[str, str]:
    """Get the repository's discussion categories."""
    categories = {}

    for node in get_repo()["data"]["repository"]["discussionCategories"]["nodes"]:
        categories[node["name"].lower()] = node["id"]

    return categories


@functools.lru_cache
def get_repo() -> dict:
    """Get basic repo info in order to ger various ID needed later for graphQL calls."""
    query = Template(
        """{
    repository(owner: "$repo_owner", name: "$repo_name") {
      id
      discussionCategories(first: 10) {
          nodes {
            id # CategoryID
            name
          }
        }
    }
    }"""
    ).substitute(repo_owner=REPO_OWNER, repo_name=REPO_NAME)
    r = requests.post("https://api.github.com/graphql", json={"query": query}, auth=("token", TOKEN))
    return r.json()
