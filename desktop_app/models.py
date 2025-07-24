from db import get_connection

# User functions
def add_user(username, password, role):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

# Patient functions
def add_patient(patient_id, name, gender, dob, phone, address, allergies, notes):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO patients (patient_id, name, gender, dob, phone, address, allergies, notes, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))''',
              (patient_id, name, gender, dob, phone, address, allergies, notes))
    conn.commit()
    conn.close()

def get_patient_by_id(patient_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
    patient = c.fetchone()
    conn.close()
    return patient

def list_patients():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM patients ORDER BY created_at DESC')
    patients = c.fetchall()
    conn.close()
    return patients 