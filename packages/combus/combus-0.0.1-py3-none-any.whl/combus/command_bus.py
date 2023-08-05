from combus.command import Command
from combus.command_handler import CommandHandler


class CommandBus:
    def __init__(self):
        """Initialize yo"""
        self.handlers = {}

    def handle(self, command: Command):
        """Handle command if linked with handler"""
        handler_name = type(command).__name__
        if handler_name in self.handlers:
            self.handlers[handler_name](command)

    def link_command_with_handler(self, command: str, handler: CommandHandler):
        """Add command handler to the commandBus.
        This will overwrite any previous handler set with the same name."""
        self.handlers[command] = handler
