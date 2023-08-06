"""Decorators and configuration file loading for the CLI."""

import os
import sys

import toml

from ..lists.load import get_list
from ..lists import InvalidConfigError

CONFIG_FILES = [
    'task_forge.toml',
    os.path.join(os.getenv('HOME', ''), '.taskforge.d', 'config.toml'),
    '/etc/taskforge.d/config.toml'
]


def default_config():
    """Return a dict with the default config values."""
    return {
        'list': {
            'name': 'sqlite',
            'config': {
                'directory': '~/.taskforge.d'
            }
        },
        'server': {
            'port': 8080,
            'list': {
                'name': 'sqlite',
                'config': {
                    'directory': '~/.taskforge.d'
                }
            }
        }
    }


def load_config():
    """Load the config file from the default locations."""
    for filename in CONFIG_FILES:
        if os.path.isfile(filename):
            with open(filename) as config_file:
                return toml.load(config_file)
    return default_config()


def config(func):
    """Load config and inject it as the keyword argument cfg."""
    cfg = load_config()

    def wrapper(*args, **kwargs):
        kwargs['cfg'] = cfg
        return func(*args, **kwargs)

    return wrapper


def load_list(cfg):
    """Load the correct List implementation based on the provided config."""
    impl = get_list(cfg['list']['name'])
    if impl is None:
        print('unknown list: {}'.format(cfg['list']['name']))
        sys.exit(1)

    try:
        return impl(**cfg['list']['config'])
    except InvalidConfigError as invalid_config:
        print('Invalid config: {}'.format(invalid_config))
        sys.exit(1)
    except TypeError as unknown_key:
        print('Invalid config unknown config key: {}'.format(unknown_key))
        sys.exit(1)


def inject_list(func):  # noqa: D202
    """Injects a kwarg task_list which contains a configured list object."""

    @config
    def wrapper(*args, **kwargs):
        kwargs['task_list'] = load_list(kwargs['cfg'])
        del kwargs['cfg']
        return func(*args, **kwargs)

    return wrapper
