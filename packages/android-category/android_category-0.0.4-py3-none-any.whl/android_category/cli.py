"""Command Line Interface for Android Category."""

import logging
import click

from android_category.android_category import get_app_category_from_repo_git, get_app_category_from_local
@click.command()
@click.argument('repo')
@click.option('--url/--local', default=True, is_flag=True, help="Whether the repo is git URL or a local directory.")
@click.option('--log', help="Specify log level (DEBUG|INFO|WARNING|ERROR|CRITICAL).")
def tool(repo, url, log):
    """CLI to retrieve a category of an app."""
    if log:
        log_numeric_level = getattr(logging, log.upper())
        logging.basicConfig(level=log_numeric_level)
    # category = collect_category_for_local_app(repo)
    # click.secho(category, fg='green')
    if url:
        category = get_app_category_from_repo_git(repo)
    else:
        category = get_app_category_from_local(repo)
    print(category)

if __name__ == '__main__':
    tool() # pylint: disable=no-value-for-parameter
