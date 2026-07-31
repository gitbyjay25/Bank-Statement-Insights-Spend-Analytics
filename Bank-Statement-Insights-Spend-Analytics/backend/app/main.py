from fastapi import FastAPI
from app.services.parsing.csv_parser import parse_csv

app = FastAPI()

@app.get('/')
def root():
    return {'status' : 'ok'}


from fastapi import FastAPI, UploadFile, File
from app.services.parsing.csv_parser import parse_csv
from app.services.parsing.pdf_parser import parse_pdf


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
    
    return [t.dict() for t in transactions]

    