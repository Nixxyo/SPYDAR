from core.destruct import trigger_self_destruct

MAX_ATTEMPTS = 3
PASSWORD = "nihar"
attempts = 0

def authenticate():
    global attempts
    while attempts < MAX_ATTEMPTS:
        user_input = input("Enter password: ")
        if user_input == PASSWORD:
            print("Access granted.")
            return True
        else:
            attempts += 1
            print(f"Incorrect! Attempt {attempts}/{MAX_ATTEMPTS}")
    print("Too many incorrect attempts.")
    trigger_self_destruct()
    return False
