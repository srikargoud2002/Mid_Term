from app.commands import Command
from app.plugins.history_facade import HistoryFacade

class HistoryClearCommand(Command):
    def execute(self):
        HistoryFacade.clear_history()
        print("Operation history cleared")