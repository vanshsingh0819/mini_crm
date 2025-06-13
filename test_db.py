from flask import Flask
from app import create_app, mysql

app = create_app()

with app.app_context():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SHOW TABLES;")
        tables = cur.fetchall()
        print("✅ Successfully connected. Tables in DB:")
        for table in tables:
            print(f" - {table[0]}")
        cur.close()
    except Exception as e:
        print("❌ Error connecting to database:", e)
