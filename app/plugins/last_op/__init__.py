from app.commands import Command
from app.plugins.history_facade import HistoryFacade

class LastOpCommand(Command):
    def execute(self):
        formatted_op = HistoryFacade.get_last_formatted()
        print(f"Last operation: {formatted_op}")
