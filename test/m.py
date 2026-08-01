import requests

path = r'C:\Users\jagdi\Desktop\BSISA\test\test_statement.csv'

with open(path, 'rb') as f:
    files = {'file': f}
    response = requests.post('http://127.0.0.1:8000/upload', files=files)
    statement_id = response.json()['statement_id']
    print(f"Statement ID: {statement_id}")

response = requests.get(f'http://127.0.0.1:8000/analytics/{statement_id}')
print(response.json())