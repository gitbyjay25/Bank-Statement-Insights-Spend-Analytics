from datetime import date
from enum import Enum
from pydantic import BaseModel


class TransactionType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class Transaction(BaseModel):
    txn_date: date
    description: str
    amount: float
    txn_type: TransactionType
    category: str = None
    confidence_score: float = None