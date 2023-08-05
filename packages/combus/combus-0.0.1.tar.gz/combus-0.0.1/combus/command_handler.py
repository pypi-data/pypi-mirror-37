from combus.command import Command


class CommandHandler:
    def __call__(self, command: Command):
        self._handle(command)

    def _handle(self, command: Command):
        raise NotImplementedError()
