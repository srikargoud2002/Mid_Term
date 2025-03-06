from calculator.history.history import OperationHistory
from datetime import datetime
from pathlib import Path
import pandas as pd
from calculator.operations import add_numbers, sub_numbers, mul_numbers, div_numbers
from calculator.calculation import OperationRecord
from decimal import Decimal, InvalidOperation
import logging
import os
from dotenv import load_dotenv
from logging_custom.logging_config import LoggingConfig

load_dotenv()
logger = logging.getLogger(__name__)
class HistoryFacade:

    @staticmethod
    def _get_history_dir() -> Path:
        """Get history directory from environment variable, create if needed"""
        history_dir = Path(os.getenv('HISTORY_PATH', 'calculator_history'))  # Default directory
        logger.debug(f"Using history directory: {history_dir}")
        try:
            history_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created history directory at {history_dir.absolute()}")
        except PermissionError as pe:
            logger.critical(f"Permission denied creating history directory: {pe}")
            raise RuntimeError(f"Permission denied creating history directory: {pe}") from pe
        return history_dir

    @staticmethod
    def get_formatted_history():
        """Get history with human-readable formatting"""
        logger.debug("Formatting calculation history")
        return [
            f"{record.x} {record.symbol} {record.y} = {record.execute()}"
            for record in OperationHistory.get_all_records()
        ]
    
    @staticmethod
    def clear_history():
        """Facade method to Clear"""
        logger.info("Clearing operation history")
        OperationHistory.clear_records()
    
    @staticmethod
    def get_last_formatted() -> str:
        """Facade method to get formatted last operation"""
        logger.debug("Retrieving last formatted operation")
        record = OperationHistory.get_last_record()
        if not record:
            logger.warning("No operations found in history")
            return "No operations in history"
        return f"{record.x} {record.symbol} {record.y} = {record.execute()}"
        
    @staticmethod
    def save_to_csv():
        """Save history with timestamped filename to configured directory"""
        history_dir = HistoryFacade._get_history_dir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"calculator_history_{timestamp}.csv"
        filepath = history_dir / filename
        records = OperationHistory.get_all_records()
        
        if not records:
            logger.warning("Attempted to save empty history")
            return "No history to save"
        logger.info(f"Saving {len(records)} records to {filepath}")
                    
        df = pd.DataFrame([{
            'operand1': str(r.x),
            'operand2': str(r.y),
            'operation': r.symbol,
            'result': str(r.execute())
        } for r in records])
        
        df.to_csv(filepath, index=False)
        logger.debug(f"CSV file created successfully at {filepath}")
        return f"History saved to {filepath.absolute()}"


    @staticmethod
    def list_csv_files():
        """List all CSV files in history directory"""
        try:
            history_dir = HistoryFacade._get_history_dir()
            files = [f for f in history_dir.glob('*.csv') if f.is_file()]
            logger.debug(f"Found {len(files)} CSV files in history directory")
            return files
        except Exception as e:
            logger.error(f"Error listing CSV files: {str(e)}")
            return []

    @staticmethod
    def load_from_csv(filename: str) -> str:
        """Load history from CSV and return formatted entries"""
        try:
            # Validate file existence
            logger.info(f"Attempting to load history from {filename}")
            history_dir = HistoryFacade._get_history_dir()
            filepath = history_dir / filename
            if not filepath.exists():
                logger.error(f"CSV file not found: {filepath}")
                return f"Error: File '{filepath}' not found"

            # Read CSV with required columns
            df = pd.read_csv(
                filepath,
                usecols=['operand1', 'operand2', 'operation', 'result']
            )

            # Clear existing history
            OperationHistory.clear_records()
            logger.info("Cleared existing history before import")

            # Operation symbol mapping
            operation_map = {
                '+': add_numbers,
                '-': sub_numbers,
                '×': mul_numbers,
                '÷': div_numbers
            }

            # Process records
            loaded_count = 0
            for _, row in df.iterrows():
                try:
                    # Convert and validate data
                    x = Decimal(str(row['operand1']))
                    y = Decimal(str(row['operand2']))
                    op_func = operation_map[row['operation']]
                    
                    # Create and store record
                    record = OperationRecord.create(x, y, op_func)
                    OperationHistory.add_record(record)
                    loaded_count += 1
                    
                except (KeyError, ValueError, InvalidOperation):
                    logger.warning(f"Skipping invalid record: {row.to_dict()} - Error: {str(e)}")
                    continue

            # Get formatted history
            formatted = HistoryFacade.get_formatted_history()
            logger.info(f"Successfully loaded {loaded_count} records from {filename}")
            
            # Build result message
            result = [f"Loaded {loaded_count} entries from '{filename}':"]
            result += [f"{i+1}. {entry}" for i, entry in enumerate(formatted)]
            
            return "\n".join(result)

        except pd.errors.EmptyDataError:
            logger.error("Attempted to load empty CSV file")
            return "Error: CSV file is empty"
        except pd.errors.ParserError:
            logger.error(f"CSV parsing failed: {str(e)}")
            return "Error: Invalid CSV format"
        except KeyError as e:
            logger.error(f"Missing required column: {str(e)}")
            return f"Error: Missing column {str(e)}"
        except Exception as e:
            logger.exception("Critical error loading CSV history")
            return f"Loading failed: {str(e)}"
        