from fastapi import FastAPI, UploadFile, File
from app.services.parsing.csv_parser import parse_csv
from app.services.parsing.pdf_parser import parse_pdf
from app.db.connection import save_statement, save_transactions
from app.services.categorization.categorizer import categorize_transaction
from app.services.analytics.analytics import get_spend_by_category, get_surplus
from app.services.advisory.advisor import generate_advisory


app = FastAPI()


@app.get('/')
def root():
    return {'status': 'ok'}


@app.post('/upload')
async def upload_statement(file: UploadFile = File(...)):
    file_extension = file.filename.split('.')[-1].lower()
    file_content = await file.read()
    
    if file_extension == 'csv':
        content_str = file_content.decode('utf-8')
        transactions = parse_csv(content_str)
    elif file_extension == 'pdf':
        transactions = parse_pdf(file_content)
    else:
        return {'error': 'Unsupported file format'}
    
    for txn in transactions:
        category, confidence = categorize_transaction(txn.description)
        txn.category = category
        txn.confidence_score = confidence
    
    statement_id = save_statement(file.filename)
    save_transactions(statement_id, transactions)
    
    return {
        'statement_id': statement_id,
        'transactions_count': len(transactions),
        'transactions': [t.dict() for t in transactions]
    }


@app.get('/analytics/{statement_id}')
def get_analytics(statement_id: int):
    spend_by_category = get_spend_by_category(statement_id)
    surplus = get_surplus(statement_id)
    recommendations = generate_advisory(statement_id)
    
    return {
        'statement_id': statement_id,
        'spend_by_category': spend_by_category,
        'financial_summary': surplus,
        'recommendations': recommendations
    }