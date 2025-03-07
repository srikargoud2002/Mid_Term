from app.plugins.history_clear import HistoryClearCommand
from calculator.history.history import OperationHistory
from app.plugins.last_op import LastOpCommand

from calculator.calculation import OperationRecord
from calculator.operations import add_numbers
from decimal import Decimal
from app.plugins.history_facade import HistoryFacade
from app.plugins.history_show import HistoryShowCommand


def test_history_clear_command():
    # Add a dummy operation to history
    record = OperationRecord.create(Decimal('1'), Decimal('2'), add_numbers)
    OperationHistory.add_record(record)
    assert len(OperationHistory.get_all_records()) == 1

    # Execute the HistoryClearCommand
    command = HistoryClearCommand()
    command.execute()

    # Verify history is cleared
    assert len(OperationHistory.get_all_records()) == 0

def test_no_history():
    OperationHistory.clear_records()
    assert HistoryFacade.get_formatted_history() == []
    assert HistoryFacade.get_last_formatted() == "No operations in history"
    assert HistoryFacade.save_to_csv() == "No history to save"

def test_history_show_command_no_history(capsys):
    # Ensure history is empty
    OperationHistory.clear_records()
    assert len(OperationHistory.get_all_records()) == 0

    # Execute HistoryShowCommand
    command = HistoryShowCommand()
    command.execute()

    # Capture printed output
    captured = capsys.readouterr()
    assert captured.out.strip() == "No history available"

def test_history_last_command_no_history(capsys):
    # Ensure history is empty
    OperationHistory.clear_records()

    command = LastOpCommand()
    command.execute()

    captured = capsys.readouterr()
    assert captured.out.strip() == "Last operation: No operations in history"

def test_history_last_command_with_history(capsys):
    # Add a sample operation to history
    record = OperationRecord.create(Decimal('3'), Decimal('4'), add_numbers)
    OperationHistory.add_record(record)

    # Execute command
    command = LastOpCommand()
    command.execute()

    captured = capsys.readouterr()
    assert captured.out.strip() == "Last operation: 3 + 4 = 7"