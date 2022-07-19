# -*- coding: utf-8 -*-
"""Utilities."""

import functools
import os
from string import Template
from typing import Any, Dict

import click
import requests
from decouple import config
from loguru import logger

REPO_OWNER = config("REPO_OWNER")
REPO_NAME = config("REPO_NAME")
REPO = f"{REPO_OWNER}/{REPO_NAME}"
REPO_URL = f"https://api.github.com/repos/{REPO}"
TOKEN = config("TOKEN")


def make_request(url: str, headers: dict, auth: Any, request_type: str = "post") -> dict:
    """Make a generic request."""
    if request_type == "post":
        r = requests.post(url, headers=headers, auth=auth)
    elif request_type == "get":
        r = requests.get(url, headers=headers, auth=auth)

    r.raise_for_status()

    return r.json()


def create_discussion(title: str, open_obj: str, category_name: str) -> None:
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
          # input type: CreateDiscussionInput
            createDiscussion(input: {
                repositoryId: "$repo_id",
                categoryId: "$category_id",
                body: "The body", title: "$title"}) {
            # response type: CreateDiscussionPayload
            discussion {
              id, url
            }
          }
        }
        """
    ).substitute(repo_id=repo_id, category_id=category_id, title=title)
    logger.info(f"Creating discussion with {query}")
    r = requests.post(
        "https://api.github.com/graphql", json={"query": query}, headers=headers, auth=("token", TOKEN)
    )
    d = r.json()
    url = d["data"]["createDiscussion"]["discussion"]["url"]
    click.echo(f"Created discussion {url}")

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
