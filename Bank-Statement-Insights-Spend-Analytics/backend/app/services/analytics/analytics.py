from app.db.connection import get_connection


def get_spend_by_category(statement_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT category, SUM(amount) as total, COUNT(*) as count
        FROM transactions
        WHERE statement_id = %s AND txn_type = 'debit'
        GROUP BY category
    """, (statement_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def get_surplus(statement_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            SUM(CASE WHEN txn_type = 'credit' THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN txn_type = 'debit' THEN amount ELSE 0 END) as expenses
        FROM transactions
        WHERE statement_id = %s
    """, (statement_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    income = result['income'] or 0
    expenses = result['expenses'] or 0
    return {'income': income, 'expenses': expenses, 'surplus': income - expenses}