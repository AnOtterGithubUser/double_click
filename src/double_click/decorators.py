from .command import CommandWithConfig
from click.core import Command
from click.decorators import _check_for_unicode_literals
import inspect


def _make_command_with_config(f, config_file_path, name, attrs):
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
    return CommandWithConfig(name=name or f.__name__.lower().replace('_', '-'), config_filepath=config_file_path,
                             callback=f, params=params, **attrs)


def command_with_config(config_file_path, name=None, **attrs):
    def decorator(f):
        cmd = _make_command_with_config(f, config_file_path, name, attrs)
        cmd.__doc__ = f.__doc__
        return cmd
    return decorator

