#!/usr/bin/env python
import os
import sys
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


def process(dir_repos, repos):
    if not os.path.isdir(dir_repos):
        if not os.path.isdir(os.path.dirname(dir_repos)):
            return

        os.mkdir(dir_repos)

    os.chdir(dir_repos)

    for repo in repos.split():
        os.system('git clone {}'.format(repo))

    for d in os.listdir(dir_repos):
        repo_dir = os.path.join(dir_repos, d)
        if os.path.isdir(os.path.join(repo_dir, '.git')):
            os.chdir(repo_dir)
            os.system('git pull origin master')


def execute_from_command_line():
    try:
        config_section = sys.argv[1].split(':', 1)
    except IndexError:
        exit(1)

    config_path = config_section[0]
    section = len(config_section) >= 2 and config_section[1] or None

    config = configparser.ConfigParser()
    config.read(config_path)

    sections = section and [section] or config.sections()
    for section in sections:
        try:
            dir_repos = os.path.abspath(config.get(section, 'dir'))
            repos = config.get(section, 'repos')
        except (KeyError, configparser.NoOptionError):
            continue

        process(dir_repos, repos)


if __name__ == '__main__':
    execute_from_command_line()
