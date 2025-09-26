SPYDAR (Secure Project for Your Data Assurance & Response) is a security-focused project that combines an encrypted self-destructing diary with real-time USB intrusion detection and response.  

🚀 Features

🔒 Encrypted Diary
- AES-based encryption & decryption of diary entries.
- Password-protected access (`nihar` as default key for now).
- Self-destruct mechanism after 3 failed attempts.
- File hiding & secure storage of diary data.

🖥️ USB Intrusion Detection
- Monitors USB ports in real-time.
- Alerts/logs when unauthorized USB devices are connected.
- Trigger response mechanism (can self-destruct or lock diary).

⚙️ Core Modules
- `main.py` → Entry point for the project.
- `core/destruct.py` → Self-destruct logic.
- `core/auth.py` → Authentication and password handling.
- `core/encryption.py` → AES encryption & decryption.
- `core/entry_manager.py` → Diary entry management.
