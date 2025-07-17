# check_env.py
from dotenv import load_dotenv
import os

load_dotenv()

cred = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
print("GOOGLE_APPLICATION_CREDENTIALS =", cred)
print("Datei existiert?        ", os.path.exists(cred or ""))
