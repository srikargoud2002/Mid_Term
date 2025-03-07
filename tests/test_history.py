import pytest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from app.plugins.history_facade import HistoryFacade
from calculator.calculation import OperationRecord
from calculator.history.history import OperationHistory
from calculator.operations import add_numbers, sub_numbers, mul_numbers, div_numbers
import pandas as pd

@pytest.fixture(autouse=True)
def clear_history_before_tests():
    OperationHistory.clear_records()

@pytest.fixture
def sample_operations():
    return [
        OperationRecord.create(Decimal('10'), Decimal('5'), add_numbers),
        OperationRecord.create(Decimal('20'), Decimal('4'), sub_numbers),
        OperationRecord.create(Decimal('3'), Decimal('7'), mul_numbers),
        OperationRecord.create(Decimal('100'), Decimal('20'), div_numbers)
    ]

def test_get_formatted_history(sample_operations):
    for op in sample_operations:
        OperationHistory.add_record(op)
    formatted = HistoryFacade.get_formatted_history()
    assert formatted == [
        "10 + 5 = 15",
        "20 - 4 = 16",
        "3 × 7 = 21",
        "100 ÷ 20 = 5"
    ]

def test_clear_history(sample_operations):
    for op in sample_operations:
        OperationHistory.add_record(op)
    HistoryFacade.clear_history()
    assert len(OperationHistory.get_all_records()) == 0

def test_get_last_formatted(sample_operations):
    assert HistoryFacade.get_last_formatted() == "No operations in history"
    for op in sample_operations:
        OperationHistory.add_record(op)
    assert HistoryFacade.get_last_formatted() == "100 ÷ 20 = 5"

@patch('app.plugins.history_facade.pd.DataFrame.to_csv')
@patch('app.plugins.history_facade.HistoryFacade._get_history_dir')
def test_save_to_csv(mock_get_dir, mock_to_csv, sample_operations, tmp_path):
    mock_get_dir.return_value = tmp_path
    for op in sample_operations:
        OperationHistory.add_record(op)

    result = HistoryFacade.save_to_csv()
    
    mock_to_csv.assert_called_once()
    assert "History saved to" in result

@patch('app.plugins.history_facade.HistoryFacade._get_history_dir')
def test_list_csv_files(mock_get_dir, tmp_path):
    mock_get_dir.return_value = tmp_path
    # Explicitly create fake CSV files in tmp_path
    fake_file1 = tmp_path / 'history1.csv'
    fake_file2 = tmp_path / 'history2.csv'
    fake_file1.touch()
    fake_file2.touch()

    files = HistoryFacade.list_csv_files()
    
    assert set(files) == {fake_file1, fake_file2}

@patch('app.plugins.history_facade.pd.read_csv')
@patch('app.plugins.history_facade.HistoryFacade._get_history_dir')
def test_load_from_csv(mock_get_dir, mock_read_csv, tmp_path):
    mock_get_dir.return_value = tmp_path
    csv_file = tmp_path / "test.csv"
    csv_file.touch()  # explicitly create file to pass existence check

    mock_df = MagicMock()
    mock_df.iterrows.return_value = iter([
        (0, {'operand1': '8', 'operand2': '2', 'operation': '+', 'result': '10'}),
        (1, {'operand1': '9', 'operand2': '3', 'operation': '-', 'result': '6'}),
        (2, {'operand1': '4', 'operand2': '5', 'operation': '×', 'result': '20'}),
        (3, {'operand1': '100', 'operand2': '25', 'operation': '÷', 'result': '4'})
    ])
    
    mock_read_csv.return_value = mock_df
    
    result = HistoryFacade.load_from_csv("test.csv")
    
    expected_output_lines = [
        "Loaded 4 entries from 'test.csv':",
        "1. 8 + 2 = 10",
        "2. 9 - 3 = 6",
        "3. 4 × 5 = 20",
        "4. 100 ÷ 25 = 4"
    ]
    
    assert result == "\n".join(expected_output_lines)

@patch('app.plugins.history_facade.HistoryFacade._get_history_dir')
def test_load_from_csv_file_not_found(mock_get_dir, tmp_path):
    mock_get_dir.return_value = tmp_path
    non_existing_file = "nonexistent.csv"

    result = HistoryFacade.load_from_csv(non_existing_file)

    assert result == f"Error: File '{tmp_path / non_existing_file}' not found"

@patch('app.plugins.history_facade.pd.read_csv', side_effect=pd.errors.EmptyDataError)
@patch('app.plugins.history_facade.HistoryFacade._get_history_dir')
def test_load_from_empty_csv(mock_get_dir, mock_read_csv, tmp_path):
    mock_get_dir.return_value = tmp_path
    empty_file = tmp_path / "empty.csv"
    empty_file.touch()

    result = HistoryFacade.load_from_csv("empty.csv")

    assert result == "Error: CSV file is empty"
