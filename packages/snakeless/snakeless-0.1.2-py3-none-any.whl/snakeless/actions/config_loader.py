import fs
from schema import SchemaError

from ..helpers import snakeless_spinner, parse_config
from ..exceptions import CommandFailure


class ConfigLoaderMixin(object):
    def load_config(self, root_fs):
        with snakeless_spinner(
            text="Loading the config file...", spinner="dots"
        ) as spinner:
            try:
                config = parse_config(root_fs)
            except fs.errors.ResourceNotFound:
                raise CommandFailure("Config does not exist.")
            except SchemaError as exc:
                raise CommandFailure("Config validation failed.")
            else:
                spinner.succeed("The config file was loaded.")
                return config
