# pylint: disable=too-many-arguments

"""Automate management of Docker hub image tags."""

import os
import configparser
import requests
import semantic_version

import click

from . import __version__


USER_SECTION_KEY = 'user'


TOKEN_OPTION_KEY = 'token'


def get_token():
    """Read stored auth token."""
    cfg = os.path.join(click.get_app_dir('swabber'), 'config.ini')
    parser = configparser.RawConfigParser()
    parser.read([cfg])
    token = parser[USER_SECTION_KEY][TOKEN_OPTION_KEY]
    return token


def set_token(new_token):
    """Store auth token."""
    cfg = os.path.join(click.get_app_dir('swabber'), 'config.ini')
    parser = configparser.RawConfigParser()
    parser.read([cfg])

    try:
        parser[USER_SECTION_KEY][TOKEN_OPTION_KEY] = new_token
    except KeyError:
        parser[USER_SECTION_KEY] = {TOKEN_OPTION_KEY: new_token}

    if not os.path.exists(click.get_app_dir('swabber')):
        os.makedirs(click.get_app_dir('swabber'))
    with open(cfg, 'w') as configfile:
        parser.write(configfile)


def is_semver(text):
    """Validate SemVer.

    This is necessary because semantic_version.validate doesn't accept partial=True.
    """
    try:
        _ = semantic_version.Version(text, partial=True)
        return True
    except ValueError:
        return False


@click.group()
@click.version_option(__version__)
def main():
    """Small CLI to automate management of Docker hub image tags."""
    pass


@main.command()
@click.option('--username', '-u', help='Docker Hub username.')
@click.option('--password', '-p', help='Docker Hub password.')
def login(username, password):
    """Login to Docker Hub and store auth token."""
    request = requests.post('https://hub.docker.com/v2/users/login/',
                            json={'username': username, 'password': password})
    token = request.json()['token']
    set_token(token)


@main.command()
@click.option('--image', '-i', help='Image name.')
@click.option('--owner', '-o', help='Image\'s owner account.')
@click.option('--commit-length', '-c', help='Length of commit hash.', default=8)
@click.option('--max-commits', '-M', default=20,
              help='Number of most recent commit hashes to keep.')
@click.option('--whitelist', '-w', help='Comma concatenated whitelist of tags.')
@click.option('--minimum-version', '-m', default='0.0.0',
              help='Minimum SemVer to keep.')
def tidy(image, owner, commit_length, max_commits, whitelist, minimum_version):
    """Tidy image tags for a Docker image."""
    token = get_token()
    headers = {'Authorization': 'JWT {0}'.format(token)}
    path = ('https://hub.docker.com/v2/repositories'
            '/{0}/{1}/tags/?page_size=10000').format(owner, image)
    tags = requests.get(path, headers=headers).json()['results']

    whitelist = whitelist.split(',') if whitelist else []
    min_ver = semantic_version.Version(minimum_version, partial=True)
    versions = [tag for tag in tags if is_semver(tag['name'])]
    commits = [tag for tag in tags
               if len(tag['name']) == commit_length
               and not is_semver(tag['name'])
               and tag['name'] not in whitelist]
    commits = sorted(commits, key=lambda k: k['last_updated'], reverse=True)

    prune = []
    prune += [tag for tag in versions
              if semantic_version.Version(tag['name'], partial=True) < min_ver]
    prune += commits[max_commits:] if len(commits) > max_commits else []

    click.echo('ToDo: delete the following tags once the API supports tag deletion:')
    click.echo([tag['name'] for tag in prune])
