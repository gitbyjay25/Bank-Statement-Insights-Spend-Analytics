from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

data = [
    ['Date', 'Narration', 'Debit', 'Credit', 'Balance'],
    ['01-01-2024', 'Salary', '', '50000', '50000'],
    ['02-01-2024', 'SWIGGY BANGALORE', '500', '', '49500'],
    ['03-01-2024', 'ELECTRICITY BILL', '2000', '', '47500'],
    ['04-01-2024', 'REFUND', '', '1000', '48500'],
]

doc = SimpleDocTemplate("sample_statement.pdf", pagesize=letter)
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))
doc.build([table])
print("PDF created: sample_statement.pdf")