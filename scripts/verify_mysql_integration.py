import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pymysql
from app import create_app
from app.config import Config

print("="*70)
print(f"Testing Live Integration against: {Config.SQLALCHEMY_DATABASE_URI}")
print("="*70)

assert 'mysql' in Config.SQLALCHEMY_DATABASE_URI, "Config is not configured for MySQL!"

app = create_app()
client = app.test_client()

# 1. Login as Admin
login_res = client.post('/login', data={
    'username': 'admin',
    'password': 'Admin@123'
}, follow_redirects=True)
assert login_res.status_code == 200, f"Admin login failed: {login_res.status_code}"
print("[PASS] 1. Admin authenticated successfully.")

# 2. Add customer via Website POST /customers/new
test_email = 'rajesh.reddy.live.test@example.com'
create_res = client.post('/customers/new', data={
    'name': 'Rajesh Reddy',
    'email': test_email,
    'phone': '9123456780',
    'address': 'Jubilee Hills, Hyderabad',
    'registration_date': '2026-11-03'
}, follow_redirects=True)
assert create_res.status_code == 200, f"Customer creation failed: {create_res.status_code}"
print("[PASS] 2. Customer creation POST submitted to website successfully.")

# 3. Direct verification in MySQL database using PyMySQL
conn = pymysql.connect(
    host=os.environ.get('MYSQL_HOST', '127.0.0.1'),
    user=os.environ.get('MYSQL_USER', 'root'),
    password=os.environ.get('MYSQL_PASSWORD', 'Karthik@199'),
    port=int(os.environ.get('MYSQL_PORT', 3306)),
    database=os.environ.get('MYSQL_DATABASE', 'banking_management_system'),
    autocommit=True
)

with conn.cursor() as cur:
    cur.execute("SELECT customer_id, name, email, phone, address FROM customers WHERE email = %s", (test_email,))
    row = cur.fetchone()
    assert row is not None, "FATAL: Customer was NOT found in MySQL database!"
    cust_id = row[0]
    print(f"[PASS] 3. Direct MySQL check confirmed! Found in MySQL customers table: ID={row[0]}, Name={row[1]}, Email={row[2]}")

    # 4. Update customer via Website POST /customers/<id>/edit
    edit_res = client.post(f'/customers/{cust_id}/edit', data={
        'name': 'Rajesh Reddy Updated',
        'email': test_email,
        'phone': '9123456789',
        'address': 'HITEC City, Hyderabad',
        'registration_date': '2026-11-03'
    }, follow_redirects=True)
    assert edit_res.status_code == 200

    cur.execute("SELECT name, phone, address FROM customers WHERE customer_id = %s", (cust_id,))
    updated_row = cur.fetchone()
    assert updated_row[0] == 'Rajesh Reddy Updated', f"Customer name update did not reflect in MySQL: {updated_row}"
    assert updated_row[1] == '9123456789', f"Phone did not reflect in MySQL: {updated_row}"
    assert updated_row[2] == 'HITEC City, Hyderabad', f"Address did not reflect in MySQL: {updated_row}"
    print(f"[PASS] 4. Customer update verified directly in MySQL: Name={updated_row[0]}, Address={updated_row[2]}")

    # 5. Clean up test record from MySQL
    cur.execute("DELETE FROM customers WHERE customer_id = %s", (cust_id,))
    conn.commit()
    print("[PASS] 5. Cleanup test record verified in MySQL.")

conn.close()

print("="*70)
print("ALL E2E MYSQL REDIRECTION & INTEGRATION CHECKS PASSED PERFECTLY!")
print("="*70)
