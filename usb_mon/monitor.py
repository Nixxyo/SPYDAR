import win32com.client
import pythoncom
import datetime
import os
import time

LOG_FILE = os.path.join("logs", "usb_intrusion.log")
EVENT_COOLDOWN = 1.5  # seconds to prevent duplicate logs

# Store last event info to filter duplicates
last_event = {"action": None, "device_id": None, "time": 0}


def log_event(action, device_name, device_id, show_alert=False):
    """Log detailed info to file, simple alert to terminal."""
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{time_str}] {action}: {device_name} | ID: {device_id}\n"

    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)

  


def extract_device_info(target_instance):
    """Extract friendly USB name + DeviceID without moniker errors."""
    try:
        dependent = target_instance.Dependent
        if dependent and "DeviceID=" in dependent:
            # Extract DeviceID
            device_id = dependent.split('DeviceID="')[1].rstrip('"')
            device_id = device_id.replace("\\\\", "\\")

            # Try to get friendly name via Win32_DiskDrive
            try:
                wmi = win32com.client.GetObject("winmgmts:")
                for drive in wmi.ExecQuery("SELECT * FROM Win32_DiskDrive WHERE InterfaceType='USB'"):
                    if device_id.split("\\")[-1].lower() in drive.PNPDeviceID.lower():
                        return drive.Caption, device_id
            except Exception:
                pass

            return "USB Device", device_id
    except Exception:
        pass
    return "USB Device", "Unknown ID"


def monitor_usb():
    """Continuous USB monitoring loop. Can be run in background thread."""
    print("[USB Monitor] Starting real-time USB detection...")
    wmi = win32com.client.GetObject("winmgmts:")
    insert_event = wmi.ExecNotificationQuery(
        "SELECT * FROM __InstanceCreationEvent WITHIN 2 "
        "WHERE TargetInstance ISA 'Win32_USBControllerDevice'"
    )
    remove_event = wmi.ExecNotificationQuery(
        "SELECT * FROM __InstanceDeletionEvent WITHIN 2 "
        "WHERE TargetInstance ISA 'Win32_USBControllerDevice'"
    )

    try:
        while True:
            pythoncom.PumpWaitingMessages()

            # Handle USB insertion
            try:
                insert = insert_event.NextEvent(500)
                if insert:
                    name, device_id = extract_device_info(insert.TargetInstance)
                    now = time.time()
                    if not (last_event["action"] == "USB Inserted"
                            and last_event["device_id"] == device_id
                            and now - last_event["time"] < EVENT_COOLDOWN):
                        log_event("USB Inserted", name, device_id, show_alert=True)
                        last_event.update({"action": "USB Inserted", "device_id": device_id, "time": now})
            except Exception:
                pass

            # Handle USB removal
            try:
                remove = remove_event.NextEvent(500)
                if remove:
                    name, device_id = extract_device_info(remove.TargetInstance)
                    now = time.time()
                    if not (last_event["action"] == "USB Removed"
                            and last_event["device_id"] == device_id
                            and now - last_event["time"] < EVENT_COOLDOWN):
                        log_event("USB Removed", name, device_id, show_alert=True)
                        last_event.update({"action": "USB Removed", "device_id": device_id, "time": now})
            except Exception:
                pass

    except KeyboardInterrupt:
        print("\n[USB Monitor] Stopped by user.")


if __name__ == "__main__":
    monitor_usb()
