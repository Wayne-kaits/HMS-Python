
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    stats = {
        'total_patients': 0,
        'appointments': 0,
        'available_beds': 0,
        'pending_lab_results': 0
    }
    recent_patients = []
    appointments = []
    return render_template('dashboard.html', stats=stats, recent_patients=recent_patients, appointments=appointments, active_page='dashboard')


@app.route('/patients')
def patients():
    patients = [
        {'name': 'John Doe', 'id': 'P001', 'gender': 'Male', 'phone': '555-1234', 'registered': '2025-07-01'},
        {'name': 'Jane Smith', 'id': 'P002', 'gender': 'Female', 'phone': '555-5678', 'registered': '2025-07-02'}
    ]
    return render_template('patients.html', title='Patient Management', page_title='Patient Management', active_page='patients', patients=patients)

@app.route('/appointments')
def appointments():
    appointments = [
        {'patient': 'John Doe', 'time': '10:00 AM', 'doctor': 'Dr. Sarah Johnson', 'status': 'Confirmed'},
        {'patient': 'Jane Smith', 'time': '11:00 AM', 'doctor': 'Dr. Alex Lee', 'status': 'Pending'}
    ]
    return render_template('appointments.html', title='Appointments', page_title='Appointments', active_page='appointments', appointments=appointments)

@app.route('/pharmacy')
def pharmacy():
    medicines = [
        {'name': 'Paracetamol', 'stock': 120},
        {'name': 'Amoxicillin', 'stock': 80}
    ]
    return render_template('pharmacy.html', title='Pharmacy', page_title='Pharmacy', active_page='pharmacy', medicines=medicines)

@app.route('/laboratory')
def laboratory():
    labs = [
        {'test': 'Blood Test', 'pending': 2},
        {'test': 'X-Ray', 'pending': 0}
    ]
    return render_template('laboratory.html', title='Laboratory', page_title='Laboratory', active_page='laboratory', labs=labs)

@app.route('/wards')
def wards():
    wards = [
        {'name': 'Ward A', 'beds': 10, 'occupied': 8},
        {'name': 'Ward B', 'beds': 12, 'occupied': 6}
    ]
    return render_template('wards.html', title='Ward Management', page_title='Ward Management', active_page='wards', wards=wards)

@app.route('/billing')
def billing():
    bills = [
        {'patient': 'John Doe', 'amount': 200, 'status': 'Paid'},
        {'patient': 'Jane Smith', 'amount': 150, 'status': 'Unpaid'}
    ]
    return render_template('billing.html', title='Billing & Payments', page_title='Billing & Payments', active_page='billing', bills=bills)

@app.route('/staff')
def staff():
    staff_list = [
        {'name': 'Dr. Sarah Johnson', 'role': 'Chief Medical Officer'},
        {'name': 'Nurse Amy', 'role': 'Nurse'}
    ]
    return render_template('staff.html', title='Staff Management', page_title='Staff Management', active_page='staff', staff_list=staff_list)

@app.route('/reports')
def reports():
    reports = [
        {'title': 'Monthly Admissions', 'date': '2025-07-01'},
        {'title': 'Lab Results Summary', 'date': '2025-07-02'}
    ]
    return render_template('reports.html', title='Reports & Analytics', page_title='Reports & Analytics', active_page='reports', reports=reports)

if __name__ == '__main__':
    app.run(debug=True)
