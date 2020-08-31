from .command import CommandWithConfig
from click.core import Command
from click.decorators import _check_for_unicode_literals
import inspect


def _make_command_with_config(f, config_file_path, name, attrs):
    """Turn a function into a double_click.CommandWithConfig

    :param f:
    Function to turn into command
    :param config_file_path:
    Path to the config file on host machine (yaml, json, or txt)
    :param name:
    Name of the command
    :param attrs:
    Additional attributes

    :return:
    double_click.CommandWithConfig
    """
    if isinstance(f, Command):
        raise TypeError('Attempted to convert a callback into a '
                        'command twice.')
    try:
        params = f.__click_params__
        params.reverse()
        del f.__click_params__
    except AttributeError:
        params = []
    help = attrs.get('help')
    if help is None:
        help = inspect.getdoc(f)
        if isinstance(help, bytes):
            help = help.decode('utf-8')
    else:
        help = inspect.cleandoc(help)
    attrs['help'] = help
    _check_for_unicode_literals()
    return CommandWithConfig(name=name or f.__name__.lower().replace('_', '-'),
                             config_filepath=config_file_path,
                             callback=f,
                             params=params, **attrs)


def command_with_config(config_file_path, name=None, **attrs):
    """Decorator to turn a function into a double click command
    A double click command holds the properties of a click command and
    enables to use a config file

    :param config_file_path: required
    Path to the config file on host machine (yaml, json, or txt)
    :param name: default None
    Name of the double click command
    :param attrs:
    Additional attributes

    :return:
    Double click decorator
    """
    def decorator(f):
        cmd = _make_command_with_config(f, config_file_path, name, attrs)
        cmd.__doc__ = f.__doc__
        return cmd
    return decorator
