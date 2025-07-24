import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'hms.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )''')
    # Patients
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        gender TEXT,
        dob TEXT,
        phone TEXT,
        address TEXT,
        allergies TEXT,
        notes TEXT,
        created_at TEXT,
        updated_at TEXT
    )''')
    # Appointments
    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT NOT NULL,
        doctor_id INTEGER,
        department TEXT,
        time TEXT,
        status TEXT,
        notes TEXT
    )''')
    # Staff
    c.execute('''CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT,
        phone TEXT,
        email TEXT,
        shift TEXT
    )''')
    # Pharmacy
    c.execute('''CREATE TABLE IF NOT EXISTS pharmacy (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        stock INTEGER,
        supplier TEXT,
        expiry TEXT
    )''')
    # Billing
    c.execute('''CREATE TABLE IF NOT EXISTS billing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        amount REAL,
        status TEXT,
        method TEXT,
        date TEXT,
        details TEXT
    )''')
    # Laboratory
    c.execute('''CREATE TABLE IF NOT EXISTS laboratory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        test_name TEXT,
        result TEXT,
        status TEXT,
        date TEXT,
        file_path TEXT
    )''')
    # Wards
    c.execute('''CREATE TABLE IF NOT EXISTS wards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        beds INTEGER,
        occupied INTEGER
    )''')
    # Audit logs
    c.execute('''CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close() 