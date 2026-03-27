import pandas as pd
from io import BytesIO, StringIO
from datetime import datetime

def generate_csv_export(transactions):
    data = []
    for tx in transactions:
        data.append({
            'Date': tx.date.strftime('%Y-%m-%d'),
            'Description': tx.description,
            'Category': tx.category.name if tx.category else 'Uncategorized',
            'Type': tx.category.get_type_display() if tx.category else 'Expense',
            'Amount': float(tx.amount),
            'Payment Method': tx.payment_method
        })
    df = pd.DataFrame(data)
    if df.empty:
        # Return empty template
        df = pd.DataFrame(columns=['Date', 'Description', 'Category', 'Type', 'Amount', 'Payment Method'])
    return df.to_csv(index=False).encode('utf-8')

def generate_xlsx_export(transactions):
    data = []
    for tx in transactions:
        data.append({
            'Date': tx.date.strftime('%Y-%m-%d'),
            'Description': tx.description,
            'Category': tx.category.name if tx.category else 'Uncategorized',
            'Type': tx.category.get_type_display() if tx.category else 'Expense',
            'Amount': float(tx.amount),
            'Payment Method': tx.payment_method
        })
    df = pd.DataFrame(data)
    if df.empty:
        df = pd.DataFrame(columns=['Date', 'Description', 'Category', 'Type', 'Amount', 'Payment Method'])
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Transactions')
    return output.getvalue()

def generate_sample_csv():
    df = pd.DataFrame([
        {
            'date': '2024-03-24',
            'amount': 150.00,
            'category': 'Groceries',
            'type': 'EXPENSE',
            'payment_method': 'CREDIT_CARD',
            'description': 'Weekly groceries'
        },
        {
            'date': '2024-03-25',
            'amount': 2500.00,
            'category': 'Salary',
            'type': 'INCOME',
            'payment_method': 'BANK_TRANSFER',
            'description': 'Monthly paycheck'
        }
    ])
    return df.to_csv(index=False).encode('utf-8')

def parse_csv_import(file_file):
    df = pd.read_csv(file_file)
    # Normalize headers
    df.columns = [c.lower().strip() for c in df.columns]
    data = []
    for _, row in df.iterrows():
        data.append({
            'date': str(row.get('date')),
            'description': str(row.get('description', '')),
            'category_name': str(row.get('category', 'Uncategorized')),
            'category_type': str(row.get('type', 'EXPENSE')),
            'amount': row.get('amount', 0),
            'payment_method': str(row.get('payment_method', 'CASH'))
        })
    return data

def parse_xlsx_import(file_file):
    df = pd.read_excel(file_file)
    df.columns = [c.lower().strip() for c in df.columns]
    data = []
    for _, row in df.iterrows():
        data.append({
            'date': str(row.get('date')),
            'description': str(row.get('description', '')),
            'category_name': str(row.get('category', 'Uncategorized')),
            'category_type': str(row.get('type', 'EXPENSE')),
            'amount': row.get('amount', 0),
            'payment_method': str(row.get('payment_method', 'CASH'))
        })
    return data
