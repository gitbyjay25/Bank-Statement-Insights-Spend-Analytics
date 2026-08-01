import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'bank_insights')


def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'bank_insights')
        )
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None


def save_statement(filename: str, account_label: str = None):
    conn = get_connection()
    if conn is None:
        raise RuntimeError("Database connection failed. Please check your DB credentials in backend/.env")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO statements (filename, account_label) VALUES (%s, %s)",
        (filename, account_label)
    )
    conn.commit()
    statement_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return statement_id


def save_transactions(statement_id: int, transactions: list):
    conn = get_connection()
    cursor = conn.cursor()
    for txn in transactions:
        cursor.execute(
            "INSERT INTO transactions (statement_id, txn_date, description, amount, txn_type, category, confidence_score) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (statement_id, txn.txn_date, txn.description, txn.amount, txn.txn_type.value, txn.category, txn.confidence_score)
        )
    conn.commit()
    cursor.close()
    conn.close()