from click.core import Command
import os
import json
import yaml
import re


class CommandWithConfig(Command):

    def __init__(self, config_filepath='train_config.yml', *args, **kwargs):
        super(CommandWithConfig, self).__init__(*args, **kwargs)
        self.config_filepath = config_filepath

    def invoke(self, ctx):
        config_params = self._parse_config()
        for param_index, (param_name, param_value) in enumerate(ctx.params.items()):
            if not param_value:  # Default is empty, set value in config
                ctx_param_type = self._get_param_type(ctx, param_index)
                ctx.params[param_name] = self._convert_to_type(config_params[param_name], ctx_param_type)
            # else overwrite config param
        super(CommandWithConfig, self).invoke(ctx)

    def _get_param_type(self, ctx, param_index):
        return ctx.command.params[param_index].type

    def _convert_to_type(self, config_param_value, ctx_param_type):
        if ctx_param_type.name == 'float':
            param_type = float
        elif ctx_param_type.name == 'choice':
            item_type = type(ctx_param_type.choices[0])
            param_type = item_type
        elif ctx_param_type == 'integer':
            param_type = int
        elif ctx_param_type == 'path':
            if ctx_param_type.exists:
                if not os.path.isfile(config_param_value):
                    raise ValueError('The path specified in config %s does not exist' % config_param_value)
            param_type = str
        else:
            raise ValueError('The context parameter type %s was not understood' % ctx_param_type.name)
        return param_type(config_param_value)

    def _parse_config(self):
        _, config_file_extension = os.path.splitext(self.config_filepath)
        with open(self.config_filepath, 'r') as config:
            if config_file_extension == '.txt':
                config_params = {}
                line = config.readline()
                while line:
                    config_params[re.split(',:', line)[0]] = re.split(',:', line)[1]
                    line = config.readline()
            elif config_file_extension == '.json':
                config_params = json.load(config)
            elif config_file_extension == '.yml':
                config_params = yaml.load(config)
            else:
                raise ValueError("Config file extension is not recognized in click extra")
        return config_params