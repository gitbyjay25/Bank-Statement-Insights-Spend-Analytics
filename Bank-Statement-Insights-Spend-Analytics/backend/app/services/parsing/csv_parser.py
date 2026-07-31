from io import StringIO
from datetime import datetime
import pandas as pd
from app.models.transaction import Transaction, TransactionType


def parse_csv(file_content: str) -> list[Transaction]:
    df = pd.read_csv(StringIO(file_content))
    
    df.columns = df.columns.str.strip().str.lower()
    
    transactions = []
    for _, row in df.iterrows():
        txn_date = datetime.strptime(str(row['date']).strip(), '%d-%m-%Y').date()
        description = str(row['narration']).strip()
        
        debit = float(row['debit']) if pd.notna(row['debit']) and row['debit'] != '' else 0
        credit = float(row['credit']) if pd.notna(row['credit']) and row['credit'] != '' else 0
        
        if debit > 0:
            amount = debit
            txn_type = TransactionType.DEBIT
        else:
            amount = credit
            txn_type = TransactionType.CREDIT
        
        transaction = Transaction(
            txn_date=txn_date,
            description=description,
            amount=amount,
            txn_type=txn_type
        )
        transactions.append(transaction)
    
    return transactions