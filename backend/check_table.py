import sys
sys.path.insert(0, r'c:\Users\Administrator\WorkBuddy\Claw\quantai-app\backend')
from database import SessionLocal
from sqlalchemy import text
session = SessionLocal()
result = session.execute(text('SELECT sql FROM sqlite_master WHERE name="risk_settings"'))
row = result.fetchone()
if row:
    print(row[0])
else:
    print("Table not found")
session.close()