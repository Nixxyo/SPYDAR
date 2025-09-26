import threading
from core.auth import authenticate
from core.cli_runner import run_diary
from usb_mon import monitor

def start_usb_monitor():
    monitor.monitor_usb()   # ✅ Call the function, not just reference it

if __name__ == "__main__":
    # Start USB monitoring in background
    usb_thread = threading.Thread(target=start_usb_monitor, daemon=True)
    usb_thread.start()

    success = authenticate()
    if success:
        print("Welcome to Spydar Diary.")
        run_diary()  # ← Launch encrypted diary operations
