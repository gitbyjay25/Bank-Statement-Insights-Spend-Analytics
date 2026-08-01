from app.db.connection import get_connection
from decimal import Decimal


def generate_advisory(statement_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT
            SUM(CASE WHEN txn_type = 'credit' THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN txn_type = 'debit' AND category = 'Investment' THEN amount ELSE 0 END) as investment_amount,
            COUNT(CASE WHEN category = 'Investment' THEN 1 END) as investment_count
        FROM transactions
        WHERE statement_id = %s
    """, (statement_id,))
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    recommendations = []
    
    income = float(result['income'] or 0)
    investment_amount = float(result['investment_amount'] or 0)
    investment_count = result['investment_count'] or 0
    
    if investment_count == 0 and income > 0:
        recommendations.append({
            'recommendation': 'Start investing',
            'reasoning': f'No investment transactions found. Consider starting a SIP with 10-20% of income (₹{income * 0.1:.0f} - ₹{income * 0.2:.0f})',
            'estimated_impact': income * 0.08 * 12
        })
    
    return recommendations