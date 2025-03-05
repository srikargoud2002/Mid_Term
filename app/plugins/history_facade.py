from calculator.history.history import OperationHistory
from datetime import datetime
from pathlib import Path
import pandas as pd
from calculator.operations import add_numbers, sub_numbers, mul_numbers, div_numbers
from calculator.calculation import OperationRecord
from decimal import Decimal, InvalidOperation

class HistoryFacade:
    @staticmethod
    def get_formatted_history():
        """Get history with human-readable formatting"""
        return [
            f"{record.x} {record.symbol} {record.y} = {record.execute()}"
            for record in OperationHistory.get_all_records()
        ]
    
    @staticmethod
    def clear_history():
        OperationHistory.clear_records()
    
    @staticmethod
    def get_last_formatted() -> str:
        """Facade method to get formatted last operation"""
        record = OperationHistory.get_last_record()
        if not record:
            return "No operations in history"
        return f"{record.x} {record.symbol} {record.y} = {record.execute()}"
        
    @staticmethod
    def save_to_csv():
        """Save history with timestamped filename in specified format"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"calculator_history_{timestamp}.csv"
        records = OperationHistory.get_all_records()
        
        if not records:
            return "No history to save"
                    
        df = pd.DataFrame([{
            'operand1': str(r.x),
            'operand2': str(r.y),
            'operation': r.symbol,
            'result': str(r.execute())
        } for r in records])
        
        df.to_csv(filename, index=False)
        return f"History saved to {Path(filename).absolute()}"

    @staticmethod
    def list_csv_files():
        """List all CSV files in current directory"""
        return [f for f in Path('.').glob('*.csv') if f.is_file()]

    @staticmethod
    def load_from_csv(filename: str) -> str:
        """Load history from CSV and return formatted entries"""
        try:
            # Validate file existence
            if not Path(filename).exists():
                return f"Error: File '{filename}' not found"

            # Read CSV with required columns
            df = pd.read_csv(
                filename,
                usecols=['operand1', 'operand2', 'operation', 'result']
            )

            # Clear existing history
            OperationHistory.clear_records()

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
                    continue

            # Get formatted history
            formatted = HistoryFacade.get_formatted_history()
            
            # Build result message
            result = [f"Loaded {loaded_count} entries from '{filename}':"]
            result += [f"{i+1}. {entry}" for i, entry in enumerate(formatted)]
            
            return "\n".join(result)

        except pd.errors.EmptyDataError:
            return "Error: CSV file is empty"
        except pd.errors.ParserError:
            return "Error: Invalid CSV format"
        except KeyError as e:
            return f"Error: Missing column {str(e)}"
        except Exception as e:
            return f"Loading failed: {str(e)}"