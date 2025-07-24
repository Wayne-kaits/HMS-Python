import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QStackedWidget, QListWidget, QListWidgetItem, QFrame, QSizePolicy, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import os
from PyQt5.QtSvg import QSvgWidget
from db import init_db
from models import get_user_by_username, add_user
from utils import hash_password, check_password

MODULES = [
    ("Dashboard", "dashboard"),
    ("Patient Management", "patients"),
    ("Appointments", "appointments"),
    ("Pharmacy", "pharmacy"),
    ("Laboratory", "laboratory"),
    ("Ward Management", "wards"),
    ("Billing & Payments", "billing"),
    ("Staff Management", "staff"),
    ("Reports & Analytics", "reports"),
]

ICON_PATHS = {
    "dashboard": "icons/dashboard.svg",
    "patients": "icons/patient.svg",
    "appointments": "icons/calendar.svg",
    "pharmacy": "icons/pharmacy.svg",
    "laboratory": "icons/lab.svg",
    "wards": "icons/bed.svg",
    "billing": "icons/billing.svg",
    "staff": "icons/staff.svg",
    "reports": "icons/reports.svg",
    "emergency": "icons/emergency.svg",
    "newpatient": "icons/add_user.svg",
    # Stat card icons
    "stat_patients": "icons/stat_patients.svg",
    "stat_appointments": "icons/stat_appointments.svg",
    "stat_beds": "icons/stat_beds.svg",
    "stat_lab": "icons/stat_lab.svg",
}

class Sidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(220)
        self.setStyleSheet("""
            #sidebar { background: #22314A; color: white; border-top-right-radius: 20px; }
            QPushButton { color: white; text-align: left; padding: 10px 20px; border: none; border-radius: 8px; font-size: 15px; }
            QPushButton[selected="true"] { background: #1EB980; color: white; }
            QPushButton:hover { background: #2a4066; }
            QLabel#sidebarTitle { font-size: 22px; font-weight: bold; margin: 20px 0 30px 20px; }
            QLabel#quickActions { margin: 30px 0 10px 20px; font-size: 13px; color: #b0b8c1; }
            QPushButton#quick { font-size: 15px; font-weight: bold; margin: 5px 20px; }
            QPushButton#quick#emergency { background: #1EB980; color: white; }
            QPushButton#quick#newpatient { background: #2563eb; color: white; }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.title = QLabel("MediCore HMS", self)
        self.title.setObjectName("sidebarTitle")
        layout.addWidget(self.title)
        self.buttons = []
        for i, (label, key) in enumerate(MODULES):
            btn = QPushButton(f"  {label}", self)
            btn.setProperty("module_key", key)
            btn.setCheckable(True)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            icon_path = ICON_PATHS.get(key)
            if icon_path and os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
                btn.setIconSize(Qt.QSize(20, 20))
            layout.addWidget(btn)
            self.buttons.append(btn)
        layout.addSpacing(20)
        quick_label = QLabel("QUICK ACTIONS", self)
        quick_label.setObjectName("quickActions")
        layout.addWidget(quick_label)
        self.quick_emergency = QPushButton("  Emergency Admission", self)
        self.quick_emergency.setObjectName("quick")
        self.quick_emergency.setProperty("id", "emergency")
        if os.path.exists(ICON_PATHS["emergency"]):
            self.quick_emergency.setIcon(QIcon(ICON_PATHS["emergency"]))
            self.quick_emergency.setIconSize(Qt.QSize(20, 20))
        layout.addWidget(self.quick_emergency)
        self.quick_newpatient = QPushButton("  New Patient", self)
        self.quick_newpatient.setObjectName("quick")
        self.quick_newpatient.setProperty("id", "newpatient")
        if os.path.exists(ICON_PATHS["newpatient"]):
            self.quick_newpatient.setIcon(QIcon(ICON_PATHS["newpatient"]))
            self.quick_newpatient.setIconSize(Qt.QSize(20, 20))
        layout.addWidget(self.quick_newpatient)
        layout.addStretch(1)

class TopBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topbar")
        self.setStyleSheet("""
            #topbar { background: white; border-bottom: 1px solid #e5e7eb; }
            QLineEdit { border-radius: 8px; border: 1px solid #e5e7eb; padding: 6px 12px; font-size: 15px; }
            QLabel#profileName { font-weight: bold; font-size: 15px; }
            QLabel#profileRole { color: #6b7280; font-size: 12px; }
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 8, 30, 8)
        layout.setSpacing(20)
        self.search = QLineEdit(self)
        self.search.setPlaceholderText("Search patients, appointments...")
        self.search.setFixedWidth(320)
        layout.addWidget(self.search)
        layout.addStretch(1)
        self.notification = QLabel(self)
        self.notification.setPixmap(QPixmap(32, 32))  # Placeholder for icon
        layout.addWidget(self.notification)
        self.profile_pic = QLabel(self)
        self.profile_pic.setPixmap(QPixmap(40, 40))  # Placeholder for avatar
        self.profile_pic.setFixedSize(40, 40)
        self.profile_pic.setStyleSheet("border-radius: 20px; background: #eee;")
        layout.addWidget(self.profile_pic)
        profile_info = QVBoxLayout()
        self.profile_name = QLabel("Dr. Sarah Johnson", self)
        self.profile_name.setObjectName("profileName")
        self.profile_role = QLabel("Chief Medical Officer", self)
        self.profile_role.setObjectName("profileRole")
        profile_info.addWidget(self.profile_name)
        profile_info.addWidget(self.profile_role)
        layout.addLayout(profile_info)

class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLabel#sectionTitle { font-size: 20px; font-weight: bold; margin-bottom: 10px; }
            QFrame#statCard { background: white; border-radius: 12px; border: 1px solid #e5e7eb; padding: 18px; margin-right: 18px; min-width: 200px; }
            QLabel#statLabel { color: #6b7280; font-size: 14px; }
            QLabel#statValue { font-size: 28px; font-weight: bold; }
            QLabel#statSub { font-size: 13px; }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)
        welcome = QLabel("Dashboard Overview\nWelcome back! Here's what's happening at your hospital today.", self)
        welcome.setObjectName("sectionTitle")
        layout.addWidget(welcome)
        stat_row = QHBoxLayout()
        stat_icons = [
            ICON_PATHS["stat_patients"],
            ICON_PATHS["stat_appointments"],
            ICON_PATHS["stat_beds"],
            ICON_PATHS["stat_lab"],
        ]
        for (label, value, sub, color), icon_path in zip([
            ("Total Patients", "0", "+12% from last month", "#1EB980"),
            ("Today's Appointments", "0", "0 pending", "#2563eb"),
            ("Available Beds", "0", "Low capacity", "#f59e42"),
            ("Pending Lab Results", "0", "0 urgent", "#a78bfa"),
        ], stat_icons):
            card = QFrame(self)
            card.setObjectName("statCard")
            card_layout = QVBoxLayout(card)
            icon_label = QLabel(card)
            if os.path.exists(icon_path):
                icon_label.setPixmap(QPixmap(icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            card_layout.addWidget(icon_label, alignment=Qt.AlignLeft)
            stat_label = QLabel(label, card)
            stat_label.setObjectName("statLabel")
            stat_value = QLabel(value, card)
            stat_value.setObjectName("statValue")
            stat_sub = QLabel(sub, card)
            stat_sub.setObjectName("statSub")
            stat_sub.setStyleSheet(f"color: {color};")
            card_layout.addWidget(stat_label)
            card_layout.addWidget(stat_value)
            card_layout.addWidget(stat_sub)
            stat_row.addWidget(card)
        layout.addLayout(stat_row)
        # Sectioned cards (Recent Patients, Ward Status, etc.)
        section_row = QHBoxLayout()
        left_col = QVBoxLayout()
        recent_patients = QFrame(self)
        recent_patients.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #e5e7eb; padding: 18px;")
        rp_layout = QVBoxLayout(recent_patients)
        rp_title = QLabel("Recent Patients", recent_patients)
        rp_title.setStyleSheet("font-weight: bold; font-size: 17px;")
        rp_layout.addWidget(rp_title)
        rp_layout.addWidget(QLabel("(Table placeholder)", recent_patients))
        left_col.addWidget(recent_patients)
        todays_appts = QFrame(self)
        todays_appts.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #e5e7eb; padding: 18px;")
        ta_layout = QVBoxLayout(todays_appts)
        ta_title = QLabel("Today's Appointments", todays_appts)
        ta_title.setStyleSheet("font-weight: bold; font-size: 17px;")
        ta_layout.addWidget(ta_title)
        ta_layout.addWidget(QLabel("(Table placeholder)", todays_appts))
        left_col.addWidget(todays_appts)
        section_row.addLayout(left_col)
        right_col = QVBoxLayout()
        for title in ["Ward Status", "Lab Results", "Quick Stats"]:
            card = QFrame(self)
            card.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #e5e7eb; padding: 18px;")
            cl = QVBoxLayout(card)
            t = QLabel(title, card)
            t.setStyleSheet("font-weight: bold; font-size: 17px;")
            cl.addWidget(t)
            cl.addWidget(QLabel("(Link/Stats placeholder)", card))
            right_col.addWidget(card)
        section_row.addLayout(right_col)
        layout.addLayout(section_row)

class PlaceholderPage(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel(f"{title} page coming soon...", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 22px; color: #888;")
        layout.addWidget(label)

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setModal(True)
        layout = QFormLayout(self)
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        layout.addRow("Username", self.username)
        layout.addRow("Password", self.password)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
    def get_credentials(self):
        return self.username.text(), self.password.text()

def ensure_admin_user():
    # Create a default admin user if none exists
    if not get_user_by_username("admin"):
        add_user("admin", hash_password("admin123"), "admin")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MediCore HMS Desktop")
        self.setMinimumSize(1280, 800)
        central = QWidget(self)
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        # Sidebar
        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)
        # Main content area
        content_area = QVBoxLayout()
        content_area.setContentsMargins(0, 0, 0, 0)
        content_area.setSpacing(0)
        # Top bar
        self.topbar = TopBar(self)
        content_area.addWidget(self.topbar)
        # Stacked widget for pages
        self.pages = QStackedWidget(self)
        self.page_widgets = {}
        for i, (label, key) in enumerate(MODULES):
            if key == "dashboard":
                page = DashboardPage(self)
            else:
                page = PlaceholderPage(label, self)
            self.pages.addWidget(page)
            self.page_widgets[key] = page
        content_area.addWidget(self.pages)
        main_layout.addLayout(content_area)
        # Sidebar navigation logic
        for i, btn in enumerate(self.sidebar.buttons):
            btn.clicked.connect(lambda checked, idx=i: self.set_page(idx))
        self.set_page(0)
    def set_page(self, idx):
        for i, btn in enumerate(self.sidebar.buttons):
            btn.setProperty("selected", str(i == idx).lower())
            btn.setChecked(i == idx)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self.pages.setCurrentIndex(idx)

def main():
    import sys
    from PyQt5.QtWidgets import QApplication
    init_db()
    ensure_admin_user()
    app = QApplication(sys.argv)
    # Login dialog
    login = LoginDialog()
    while True:
        if login.exec_() == QDialog.Accepted:
            username, password = login.get_credentials()
            user = get_user_by_username(username)
            if user and check_password(password, user[2]):
                break
            else:
                QMessageBox.warning(None, "Login Failed", "Invalid username or password.")
        else:
            sys.exit(0)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 