from cliff import help as cliff_help
from cliff.app import App
from cliff.commandmanager import CommandManager


class SnakelessCli(App):
    def __init__(self):
        super().__init__(
            description="Snakeless CLI",
            version="0.1.0",
            command_manager=CommandManager("snakeless.cli"),
            deferred_help=True,
        )

    def initialize_app(self, argv):
        if self.interactive_mode:  # disable interactive mode
            action = cliff_help.HelpAction(None, None, default=self)
            action(self.parser, self.options, None, None)
