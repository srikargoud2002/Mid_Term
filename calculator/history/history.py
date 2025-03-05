from typing import List, Optional
from calculator.calculation import OperationRecord

class OperationHistory:
    records: List[OperationRecord] = []

    @classmethod
    def add_record(cls, record: OperationRecord) -> None:
        cls.records.append(record)

    @classmethod
    def get_all_records(cls) -> List[OperationRecord]:
        return cls.records

    @classmethod
    def get_last_record(cls) -> Optional[OperationRecord]:
        if cls.records:
            return cls.records[-1]
        else:
            return None

    @classmethod
    def clear_records(cls) -> None:
        cls.records.clear()
