import json
import yaml
import os

from dclick.command import CommandWithConfig


def test__parse_config_should_return_a_dict_of_parameters_given_a_txt_file(tmpdir):
    # Given
    content = {'a': 1, 'b': True, 'c': 'that', 'd': 1.5}
    config_filepath = os.path.join(tmpdir, 'test_config.txt')
    with open(config_filepath, 'w') as config_file:
        for param_name, param_value in content.items():
            config_file.write('%s: %s\n' % (param_name, param_value))
    test_command = CommandWithConfig(config_filepath, 'test_config_txt')
    expected_config_parameters = {'a': '1', 'b': 'True', 'c': 'that', 'd': '1.5'}
    # When
    actual_config_parameters = test_command._parse_config()
    # Then
    assert expected_config_parameters == actual_config_parameters


def test__parse_config_should_return_a_dict_of_parameters_given_a_yml_file(tmpdir):
    # Given
    content = {'a': 1, 'b': True, 'c': 'that', 'd': 1.5}
    config_filepath = os.path.join(tmpdir, 'test_config.yml')
    with open(config_filepath, 'w') as config_file:
        yaml.dump(content, config_file)
    test_command = CommandWithConfig(config_filepath, 'test_config_yml')
    expected_config_parameters = content
    # When
    actual_config_parameters = test_command._parse_config()
    # Then
    assert expected_config_parameters == actual_config_parameters


def test__parse_config_should_return_a_dict_of_parameters_given_a_json_file(tmpdir):
    # Given
    content = {'a': 1, 'b': True, 'c': 'that', 'd': 1.5}
    config_filepath = os.path.join(tmpdir, 'test_config.json')
    with open(config_filepath, 'w') as config_file:
        json.dump(content, config_file)
    test_command = CommandWithConfig(config_filepath, 'test_config_json')
    expected_config_parameters = content
    # When
    actual_config_parameters = test_command._parse_config()
    # Then
    assert expected_config_parameters == actual_config_parameters
