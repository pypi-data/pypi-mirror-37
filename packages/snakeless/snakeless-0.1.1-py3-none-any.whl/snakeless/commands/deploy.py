import logging

import fs
from cliff.command import Command

from ..constants import CURRENT_DIR
from ..actions import DeployerMixin, ConfigLoaderMixin


class Deploy(Command, DeployerMixin, ConfigLoaderMixin):
    "Deploy some functions or all of themn"

    logger = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            "-f", nargs="*", default=".", help="A list of functions' names"
        )
        return parser

    def take_action(self, parsed_args):
        parsed_args = vars(parsed_args)
        functions_to_deploy = parsed_args.get('f', [])
        with fs.open_fs(CURRENT_DIR) as root_fs:
            try:
                config = self.load_config(root_fs)
                if not functions_to_deploy:
                    functions_to_deploy = config['functions'].keys()
                self.deploy_functions(config, functions_to_deploy)
            except Exception as exc:
                self.logger.exception(exc, exc_info=True)
