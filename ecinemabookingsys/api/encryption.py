from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

fernet = Fernet(os.environ.get('ENCRYPTION_KEY').encode())

def encrypt(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

def decrypt(value: str) -> str:
    return fernet.decrypt(value.encode()).decode()