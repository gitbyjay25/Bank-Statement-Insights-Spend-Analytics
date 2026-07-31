import pdfplumber
from io import BytesIO
from datetime import datetime
from app.models.transaction import Transaction, TransactionType


def parse_pdf(file_bytes: bytes) -> list[Transaction]:
    transactions = []
    
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            
            if not table:
                continue
            
            headers = [str(h).strip().lower() for h in table[0]]
            
            for row in table[1:]:
                if not any(row):
                    continue
                
                row_dict = {headers[i]: row[i] for i in range(len(headers))}
                
                txn_date = datetime.strptime(str(row_dict.get('date', '')).strip(), '%d-%m-%Y').date()
                description = str(row_dict.get('narration', '')).strip()
                
                debit = float(row_dict.get('debit', 0)) if row_dict.get('debit', 0) else 0
                credit = float(row_dict.get('credit', 0)) if row_dict.get('credit', 0) else 0
                
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