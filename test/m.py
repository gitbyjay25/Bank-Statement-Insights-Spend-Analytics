import requests

path = r'C:\Users\jagdi\Desktop\BSISA\test\test_statement.csv'

with open(path, 'rb') as f:
    files = {'file': f}
    response = requests.post('http://127.0.0.1:8000/upload', files=files)
    print(response.json())