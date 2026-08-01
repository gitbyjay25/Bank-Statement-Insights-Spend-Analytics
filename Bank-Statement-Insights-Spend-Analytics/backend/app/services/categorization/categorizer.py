import requests
from app.db.connection import get_connection
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')


def get_category_from_rules(description: str):
    try:
        conn = get_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        desc_upper = description.upper()
        cursor.execute("SELECT category FROM category_rules WHERE INSTR(%s, UPPER(keyword)) > 0 LIMIT 1", (desc_upper,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result['category'] if result else None
    except Exception as e:
        print(f"Rule error: {e}")
        return None


def categorize_with_llm(description: str):
    try:
        prompt = f"Categorize: {description}. Choose from: Food & Dining, Transport, Shopping, Entertainment, Rent & Housing, Utilities, EMI & Loans, Healthcare, Investment, Income, Other. Return ONLY category name."
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "mixtral-8x7b-32768",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "max_tokens": 20
            },
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        print(f"Groq error: {response.status_code} {response.text}")
        return "Other"
    except Exception as e:
        print(f"LLM error: {e}")
        return "Other"


def save_rule_to_db(keyword: str, category: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT IGNORE INTO category_rules (keyword, category) VALUES (%s, %s)", (keyword, category))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Save rule error: {e}")


def categorize_transaction(description: str):
    rule_category = get_category_from_rules(description)
    if rule_category:
        return rule_category, 0.95
    
    llm_category = categorize_with_llm(description)
    save_rule_to_db(description.split()[0], llm_category)
    
    return llm_category or "Other", 0.80