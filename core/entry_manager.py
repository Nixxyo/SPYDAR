import os
from core.encryption import encrypt_data, decrypt_data

DIARY_PATH = "diary/encrypted_diary.txt"
PASSWORD = "nihar"

def view_entries():
    if not os.path.exists(DIARY_PATH):
        print("No diary entries found.")
        return

    with open(DIARY_PATH, 'rb') as file:
        encrypted = file.read()

    decrypted = decrypt_data(encrypted, PASSWORD)

    if decrypted is None:
        print("[❌] Failed to decrypt diary")

def add_entry():
    entry = input("Write your diary entry:\n> ")
    entry = f"\n[Entry]\n{entry}\n"

    if os.path.exists(DIARY_PATH):
        with open(DIARY_PATH, 'rb') as file:
            decrypted = decrypt_data(file.read(), PASSWORD)
            if decrypted is None:
                print("[❌] Cannot read existing entries due to decryption error.")
                return
            existing = decrypted.decode()
    else:
        existing = ""

    combined = (existing + entry).encode()
    encrypted = encrypt_data(combined, PASSWORD)

    with open(DIARY_PATH, 'wb') as file:
        file.write(encrypted)

    print("✅ Entry added successfully.")

