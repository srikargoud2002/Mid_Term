from app.commands import Command
from app.plugins.history_facade import HistoryFacade

class HistorySaveCommand(Command):
    def execute(self):
        result = HistoryFacade.save_to_csv()
        print(result)