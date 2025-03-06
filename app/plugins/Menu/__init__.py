from app.commands import Command


class MenuCommand(Command):
    def __init__(self, command_handler):
        self.command_handler = command_handler
    def execute(self):
        available_commands = list(self.command_handler.commands.keys())
        print("Available commands:")
        for command in available_commands:
            print(f"- {command}")