============
Dclick
============


.. image:: https://img.shields.io/pypi/v/dclick.svg
        :target: https://pypi.python.org/pypi/dclick

.. image:: https://circleci.com/gh/AnOtterGithubUser/double_click.svg?style=shield
        :target: https://circleci.com/gh/AnOtterGithubUser/double_click




Extend click functionnalities by allowing parameters to be passed in a config file.


* Free software: BSD license


Features
--------

* Implement a new decorator 'command_with_config' which enables to pass default values for click options in a config file
* Performs the same checks as click regarding values passed in config file (ex: check if path exists)
* Seamless integration with click, just replace `click.command` with `dclick.command_with_config`

With click you would have to pass a default value directly in the code

.. code-block:: python

    from click import command
    from click import option

    @command()
    @option('-n', '--n-epochs', type=int, default=5, help='Number of epochs to train the model')
    def train(n_epochs):
        run_training_for(n_epochs)

    if __name__ == '__main__':
        train()

However, if you want to run this code with different parameters you would have to edit the code each time
or pass them in the command line. Both these solutions are not satisfying for automation and versioning.
Imagine that you want to run your code inside a docker without the possibility to use the command line,
like you are working with a managed platform on the cloud.
With `dclick` you just have to change one line:

.. code-block:: python

    from dclick import command_with_config
    from click import option

    @command_with_config('path_to_config.json')
    @option('-n', '--n-epochs', type=int)
    def train(n_epochs):
        run_training_for(n_epochs):

    if __name__ == '__main__':
        train()

Just be careful that the name in the config matches the name of the option. `dclick` takes care of the rest.
You can pass a config as json, yaml or txt. Json and yaml are preferred.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
