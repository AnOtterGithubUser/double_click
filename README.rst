============
double_click
============


.. image:: https://img.shields.io/pypi/v/double_click.svg
        :target: https://pypi.python.org/pypi/double_click

.. image:: https://circleci.com/gh/AnOtterGithubUser/double_click.svg?style=shield
        :target: https://circleci.com/gh/AnOtterGithubUser/double_click




Extend click functionnalities by allowing parameters to be passed in a config file


* Free software: BSD license


Features
--------

* Implement a new decorator 'command_with_config' which enables to pass default values for click options in a config file
* Performs the same checks as click regarding values passed in config file (ex: check if path exists)
* Seamless integration with click, just replace `click.command` with `click.command_with_config`

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
