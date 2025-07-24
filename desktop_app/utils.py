import bcrypt
import qrcode
import python_barcode
from python_barcode import Code128
from PIL import Image
from PyQt5.QtWidgets import QFileDialog

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def generate_qr_code(data, filename):
    img = qrcode.make(data)
    img.save(filename)
    return filename

def generate_barcode(data, filename):
    barcode = Code128(data, writer=python_barcode.writer.ImageWriter())
    barcode.save(filename)
    return filename

def open_file_dialog(parent, filetypes=("All Files (*.*)",)):
    dlg = QFileDialog(parent)
    dlg.setFileMode(QFileDialog.ExistingFile)
    dlg.setNameFilters([filetypes])
    if dlg.exec_():
        return dlg.selectedFiles()[0]
    return None

def save_file_dialog(parent, filetypes=("All Files (*.*)",)):
    dlg = QFileDialog(parent)
    dlg.setAcceptMode(QFileDialog.AcceptSave)
    dlg.setNameFilters([filetypes])
    if dlg.exec_():
        return dlg.selectedFiles()[0]
    return None 