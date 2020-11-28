import yaml
import json
from click.testing import CliRunner
import os
import click

from dclick import command_with_config


def test_command_with_yaml_config_decorated_function_should_work(tmpdir):
    # Given
    content = {"a": 1, "b": True, "c": "that", "d": 1.5}
    config_filepath = os.path.join(tmpdir, "test_config.yml")
    with open(config_filepath, "w") as config_file:
        yaml.dump(content, config_file)

    @command_with_config(config_filepath)
    @click.option("--a", type=float)
    @click.option("--c", type=str)
    def test_command(a, c):
        click.echo("The value of a is %s\nThe value of c is %s" % (a, c))

    runner = CliRunner()
    # When
    result = runner.invoke(test_command)
    # Then
    assert result.exit_code == 0
    assert result.output == "The value of a is 1.0\nThe value of c is that\n"


def test_command_with_json_config_decorated_function_should_work(tmpdir):
    # Given
    content = {"a": 1, "b": True, "c": "that", "d": 1.5}
    config_filepath = os.path.join(tmpdir, "test_config.json")
    with open(config_filepath, "w") as config_file:
        json.dump(content, config_file)

    @command_with_config(config_filepath)
    @click.option("--a", type=float)
    def test_command(a):
        click.echo("The value of a is %s" % a)

    runner = CliRunner()
    # When
    result = runner.invoke(test_command)
    # Then
    assert result.exit_code == 0
    assert result.output == "The value of a is 1.0\n"


def test_command_with_txt_config_decorated_function_should_work(tmpdir):
    # Given
    content = {"a": 1, "b": True, "c": "that", "d": 1.5}
    config_filepath = os.path.join(tmpdir, "test_config.txt")
    with open(config_filepath, "w") as config_file:
        for key in content:
            config_file.write("%s: %s\n" % (key, content[key]))

    @command_with_config(config_filepath)
    @click.option("--a", type=float)
    def test_command(a):
        click.echo("The value of a is %s" % a)

    runner = CliRunner()
    # When
    result = runner.invoke(test_command)
    # Then
    assert result.exit_code == 0
    assert result.output == "The value of a is 1.0\n"


def test_command_with_integer_type_should_work(tmpdir):
    # Given
    content = {"i": 5}
    config_filepath = os.path.join(tmpdir, "test_config.yml")
    with open(config_filepath, "w") as config_file:
        yaml.dump(content, config_file)

    @command_with_config(config_filepath)
    @click.option("--i", type=int)
    def test_command_integer_type(i):
        click.echo("The value of the integer is %s" % i)

    runner = CliRunner()
    # When
    result = runner.invoke(test_command_integer_type)
    # Then
    assert result.exit_code == 0
    assert result.output == "The value of the integer is 5\n"


def test_command_with_existing_path_should_work(tmpdir):
    # Given
    config_filepath = os.path.join(tmpdir, "test_config.yml")
    test_path = os.path.join(tmpdir, "test_path.txt")
    content = {"p": test_path}
    with open(config_filepath, "w") as config_file:
        yaml.dump(content, config_file)
    with open(test_path, "w") as test_file:
        test_file.write("Roses are red, violets are blue, it's time for a switcheroo")

    @command_with_config(config_filepath)
    @click.option("--p", type=click.Path(exists=True))
    def test_command_path_type(p):
        click.echo("The value of the path is %s" % p)

    runner = CliRunner()
    # When
    result = runner.invoke(test_command_path_type)
    # Then
    assert result.exit_code == 0
    assert result.output == "The value of the path is %s/test_path.txt\n" % tmpdir


def test_command_with_non_existing_path_should_fail(tmpdir):
    # Given
    config_filepath = os.path.join(tmpdir, "test_config.yml")
    test_path = os.path.join(tmpdir, "test_path.txt")
    content = {"p": test_path}
    with open(config_filepath, "w") as config_file:
        yaml.dump(content, config_file)

    @command_with_config(config_filepath)
    @click.option("--p", type=click.Path(exists=True))
    def test_command_path_type(p):
        click.echo("The value of the path is %s" % p)

    runner = CliRunner()
    # When
    result = runner.invoke(test_command_path_type)
    # Then
    assert result.exit_code == 1
    assert (
        result.exception.args[0]
        == "The path specified in config %s does not exist" % test_path
    )


def test_command_with_paramater_name_including_underscore(tmpdir):
    # Given
    config_filepath = os.path.join(tmpdir, "test_config.yml")
    content = {"n-epochs": 1}
    with open(config_filepath, "w") as config_file:
        yaml.dump(content, config_file)

    @command_with_config(config_filepath)
    @click.option("--n-epochs", type=int)
    def test_command_with_underscore(n_epochs):
        click.echo("The value of n_epochs is %s" % n_epochs)

    runner = CliRunner()
    # When
    result = runner.invoke(test_command_with_underscore)
    # Then
    assert result.exit_code == 0
    assert result.output == "The value of n_epochs is 1\n"


def test_command_with_shortcut_name_should_work(tmpdir):
    # Given
    config_filepath = os.path.join(tmpdir, "test_config.yml")
    content = {"parameter": "OK"}
    with open(config_filepath, "w") as config_file:
        yaml.dump(content, config_file)

    @command_with_config(config_filepath)
    @click.option("-p", "--parameter")
    def test_command_shortcut(parameter):
        click.echo("The value of parameter is %s" % parameter)

    runner = CliRunner()
    expected_output = "The value of parameter is OK\n"
    # When
    result = runner.invoke(test_command_shortcut)
    # Then
    assert result.exit_code == 0
    assert result.output == expected_output


def test_command_with_parameters_given_in_cli_should_overwrite_config_values(tmpdir):
    # Given
    config_filepath = os.path.join(tmpdir, "test_config.yml")
    content = {"a": "value", "b": "0"}
    with open(config_filepath, "w") as config_file:
        yaml.dump(content, config_file)

    @command_with_config(config_filepath)
    @click.option("--a")
    @click.option("--b")
    def test_command(a, b):
        click.echo("The value of parameter a is %s and b is %s" % (a, b))

    runner = CliRunner()
    expected_output = "The value of parameter a is changed_val and b is 2\n"
    # When
    result = runner.invoke(test_command, ["--a", "changed_val", "--b", "2"])
    # Then
    assert result.exit_code == 0
    assert result.output == expected_output


def test_command_without_config_file_should_work():
    # Given
    @command_with_config()
    @click.option("--a")
    @click.option("--b")
    def test_command(a, b):
        click.echo("The value of a is %s, the value of b is %s" % (a, b))

    runner = CliRunner()
    expected_output = "The value of a is 1, the value of b is 2\n"
    # When
    result = runner.invoke(test_command, ["--a", "1", "--b", "2"])
    # Then
    assert result.exit_code == 0
    assert result.output == expected_output
