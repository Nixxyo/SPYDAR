from core.destruct import check_password_and_handle
from core.entry_manager import view_entries, add_entry

def run_diary():
    if check_password_and_handle():
        return  

    while True:
        print("\n--- Encrypted Diary Menu ---")
        print("1. View Entries")
        print("2. Add Entry")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            view_entries()
        elif choice == "2":
            add_entry()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")
