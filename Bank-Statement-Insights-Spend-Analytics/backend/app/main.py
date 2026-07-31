from fastapi import FastAPI
from app.services.parsing.csv_parser import parse_csv

app = FastAPI()

@app.get('/')
def root():
    return {'status' : 'ok'}


@app.get('/test-csv')
def test_csv_upload():
    with open(r'C:\Users\jagdi\Desktop\BSISA\test_statement.csv','r')as f:
        file_content=f.read()
    transactions=parse_csv(file_content)
    return [t.dict() for t in transactions]


    