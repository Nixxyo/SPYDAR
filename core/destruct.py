import os
import shutil
import logging
import time
from core.encryption import decrypt_file

PASSWORD = "nihar"
SOURCE_FILE = 'diary/encrypted_diary.txt'
MOVE_DEST = r'D:/Games/encrypted_diary.txt'  # Final path will be renamed with timestamp
ATTEMPT_LIMIT = 3
LOG_FILE = 'logs/destruct.log'

logging.basicConfig(filename=LOG_FILE, level=logging.WARNING,
                    format='%(asctime)s - %(message)s')

def move_diary():
    try:
        os.makedirs(os.path.dirname(MOVE_DEST), exist_ok=True)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        dest_path = MOVE_DEST.replace(".txt", f"_{timestamp}.txt")
        shutil.move(SOURCE_FILE, dest_path)
        logging.warning(f"Diary moved after 3 failed attempts to {dest_path}")
        print("[💣] Diary destroyed !")
    except Exception as e:
        print(f"[❌] Self-destruct failed: {e}")
        logging.error(f"Failed to move diary: {e}")

def check_password_flow():
    print("[🔐] Enter password to access diary.")
    for attempt in range(ATTEMPT_LIMIT):
        pw = input("Enter password: ")
        if pw == PASSWORD:
            print("[✅] Access granted.")
            try:
                decrypted_data = decrypt_file(SOURCE_FILE, PASSWORD)
                if decrypted_data is None:
                    print("[❌] Decryption failed.")
                    return False
                if decrypted_data.strip() == "":
                    print("[⚠️] Diary is empty.")
                return True
            except Exception as e:
                print(f"[❌] Decryption failed: {str(e)}")
                return False
        else:
            print(f"[❌] Incorrect password. Attempts left: {ATTEMPT_LIMIT - attempt - 1}")
    print("[💣] Max attempts reached. Initiating self-destruct...")
    move_diary()
    return False

def trigger_self_destruct():
    check_password_flow()

def check_password_and_handle():
    return check_password_flow()
