# ghpm
Lightweight CLI for creating Github objects (e.g. issues) that help with project management and todos.

Manage your work through one of the following Github objects:

* TODO - a work item that needs to be done; implemented as a Github Issue which is closeable
* NOTE - a quick, short, note; implemented as a Github Discussion, categorized as "Ideas"
* DOC  - a deliberate, thoughtout document (cleaner than a NOTE); implemented as a Github Discussion, categorized as "General"

## Install

In order to make this CLI available to you in any virtual environment, we use [pipx](https://github.com/pypa/pipx) to install this project. To do that, first install [install pipx](https://github.com/pypa/pipx#install-pipx), then install this project with:

```
pipx install .
```

## Setup

* create a new repo and enable discussions
* create a [PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with `repo` & `write:discussion` scope
* set the ENVIRONMENT variables shown below

### Environment variables

To configure the CLI, set the ENVIRONMENT variables show in the table below.

| Variable | Description | Required | Example |
| -------- | ----------- | :-----: | -------- |
| GHPM_PAT | Github PAT created during setup | :white_check_mark: | ghp_SLFDJSzKLjf |
| GHPM_REPO_OWNER | The name of your Github user | :white_check_mark: | GithubUser |
| GHPM_REPO_NAME | The name of the repo in which objects will be created | :white_check_mark: | work_todo |
| GHPM_OPEN_URL | The URL that's opened when executing the `open` CLI command. | Not required - defaults to `https://github.com/{REPO}` where `{REPO}` is `{REPO_OWNER}/{REPO_NAME}` | |
| GHPM_DOC_CAT | The discussions category under which a **doc** will be created | Not required - defaults to `general` | |
| GHPM_NOTE_CAT | The discussions category under which a **note** will be created | Not required - defaults to `ideas` | |
