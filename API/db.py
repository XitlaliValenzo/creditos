import sqlite3

DATABASE_NAME = "api_db.db"

def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_table():
    tables =[
        """CREATE TABLE IF NOT EXISTS creditos (
                id	INTEGER NOT NULL,
                cliente	TEXT NOT NULL,
                monto	REAL NOT NULL,
                tasa_interes	REAL NOT NULL,
                plazo	INTEGER NOT NULL,
                fecha_otorgamiento	TEXT NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT))"""
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)