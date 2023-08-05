import logging

import fs
from cliff.command import Command
from schema import SchemaError

from ..constants import CURRENT_DIR
from ..helpers import (
    check_config_existence,
    snakeless_spinner,
    parse_config
)
from ..exceptions import CommandFailure


class Check(Command):
    "A health-check of your snakeless setup"

    logger = logging.getLogger(__name__)

    def check_config_existence(self, root_fs):
        with snakeless_spinner(
            text="Checking the config existence.", spinner="dots"
        ) as spinner:
            config_file_exists = check_config_existence(root_fs)
            if not config_file_exists:
                raise CommandFailure("Config was not found.")
            else:
                spinner.succeed("Config was found.")

    def validate_config(self, root_fs):
        with snakeless_spinner(
            text="Validating the config file.", spinner="dots"
        ) as spinner:
            try:
                parse_config(root_fs)
            except fs.errors.ResourceNotFound:
                raise CommandFailure("Config does not anymore exist.")
            except SchemaError as exc:
                raise CommandFailure("Config validation failed")
            else:
                spinner.succeed("Config is valid.")

    def take_action(self, parsed_args):
        with fs.open_fs(CURRENT_DIR) as root_fs:
            try:
                self.check_config_existence(root_fs)
                self.validate_config(root_fs)
            except Exception as exc:
                self.logger.exception(exc, exc_info=True)
