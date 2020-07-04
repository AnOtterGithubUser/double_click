import yaml
import json
from click.testing import CliRunner
import os
import click

from src.double_click.decorators import command_with_config


def test_command_with_yaml_config_decorated_function(tmpdir):
    # Given
    content = {'a': 1, 'b': True, 'c': 'that', 'd': 1.5}
    config_filepath = os.path.join(tmpdir, 'test_config.yml')
    with open(config_filepath, 'w') as config_file:
        yaml.dump(content, config_file)
    @command_with_config(config_filepath)
    @click.option('--a', type=float)
    def test_command(a):
        click.echo('The value of a is %s' % a)
    runner = CliRunner()
    # When
    result = runner.invoke(test_command)
    # Then
    assert result.exit_code == 0
    assert result.output == 'The value of a is 1.0\n'


def test_command_with_json_config_decorated_function(tmpdir):
    # Given
    content = {'a': 1, 'b': True, 'c': 'that', 'd': 1.5}
    config_filepath = os.path.join(tmpdir, 'test_config.json')
    with open(config_filepath, 'w') as config_file:
        json.dump(content, config_file)
    @command_with_config(config_filepath)
    @click.option('--a', type=float)
    def test_command(a):
        click.echo('The value of a is %s' % a)
    runner = CliRunner()
    # When
    result = runner.invoke(test_command)
    # Then
    assert result.exit_code == 0
    assert result.output == 'The value of a is 1.0\n'


def test_command_with_txt_config_decorated_function(tmpdir):
    # Given
    content = {'a': 1, 'b': True, 'c': 'that', 'd': 1.5}
    config_filepath = os.path.join(tmpdir, 'test_config.txt')
    with open(config_filepath, 'w') as config_file:
        for key in content:
            config_file.write('%s: %s\n' % (key, content[key]))
    @command_with_config(config_filepath)
    @click.option('--a', type=float)
    def test_command(a):
        click.echo('The value of a is %s' % a)
    runner = CliRunner()
    # When
    result = runner.invoke(test_command)
    # Then
    assert result.exit_code == 0
    assert result.output == 'The value of a is 1.0\n'
