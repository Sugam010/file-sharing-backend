import os, uuid
from cryptography.fernet import Fernet

fernet_key = Fernet.generate_key()
cipher = Fernet(fernet_key)

ALLOWED_EXTENSIONS = [".pptx", ".docx", ".xlsx"]
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def is_allowed_file(filename):
    return os.path.splitext(filename)[-1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    file_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, file_id + "_" + file.filename)
    with open(path, "wb") as buffer:
        buffer.write(file.file.read())
    return path

def encrypt_link(file_id):
    return cipher.encrypt(file_id.encode()).decode()

def decrypt_link(encrypted_str):
    return cipher.decrypt(encrypted_str.encode()).decode()
