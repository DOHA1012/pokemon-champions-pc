import os
import sys
import subprocess
import re
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import ctypes

# Set AppUserModelID to ensure the custom taskbar icon is displayed correctly on Windows
try:
    myappid = 'DOHA1012.PokemonChampions.Launcher.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

# ----------------------------------------------------
# Path helper
# ----------------------------------------------------
def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()
ADB_PATH = os.path.join(BASE_PATH, "bin", "adb", "adb.exe")
SCRCPY_PATH = os.path.join(BASE_PATH, "bin", "scrcpy", "scrcpy.exe")

# Fallback paths
if not os.path.exists(ADB_PATH):
    ADB_PATH = os.path.join(BASE_PATH, "bin", "adb.exe")
if not os.path.exists(SCRCPY_PATH):
    SCRCPY_PATH = os.path.join(BASE_PATH, "bin", "scrcpy.exe")

if not os.path.exists(ADB_PATH):
    ADB_PATH = os.path.join(BASE_PATH, "adb.exe")
if not os.path.exists(SCRCPY_PATH):
    SCRCPY_PATH = os.path.join(BASE_PATH, "scrcpy.exe")

if not os.path.exists(ADB_PATH):
    ADB_PATH = r"C:\scrcpy\adb.exe"
if not os.path.exists(SCRCPY_PATH):
    SCRCPY_PATH = r"C:\scrcpy\scrcpy.exe"

# Set ADB environment variable so scrcpy can find it
os.environ["ADB"] = ADB_PATH

# Package info
PKG_NAME = "jp.pokemon.pokemonchampions"

# ----------------------------------------------------
# Subprocess helper (Hides cmd windows)
# ----------------------------------------------------
def run_cmd(args):
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), -1

# ----------------------------------------------------
# Main GUI Class
# ----------------------------------------------------
class AppLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon Champions 무선 실행기")
        self.root.geometry("450x435")
        self.root.resizable(False, False)
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('vista')
        
        # Main Frame
        self.main_frame = ttk.Frame(self.root, padding="15")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title Label
        title_label = ttk.Label(
            self.main_frame, 
            text="Pokémon Champions Launcher", 
            font=("Malgun Gothic", 14, "bold"),
            foreground="#1e88e5"
        )
        title_label.pack(pady=(0, 15))
        
        # 1. Device Selection Frame
        dev_frame = ttk.LabelFrame(self.main_frame, text=" 1. 연결할 기기 선택 ", padding="8")
        dev_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.dev_var = tk.StringVar()
        self.cb_devices = ttk.Combobox(dev_frame, textvariable=self.dev_var, state="readonly", height=5)
        self.cb_devices.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.btn_refresh = ttk.Button(dev_frame, text="새로고침", command=self.refresh_devices)
        self.btn_refresh.pack(side=tk.RIGHT)
        
        # 2. Wireless Connect / Setup Frame
        wire_frame = ttk.LabelFrame(self.main_frame, text=" 2. 무선 연결 및 설정 ", padding="8")
        wire_frame.pack(fill=tk.X, pady=(0, 10))
        
        # IP / Port Row
        ip_row = ttk.Frame(wire_frame)
        ip_row.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(ip_row, text="무선 IP 주소:").pack(side=tk.LEFT, padx=(0, 5))
        self.txt_ip = ttk.Entry(ip_row, width=15)
        self.txt_ip.insert(0, "192.168.0.16")
        self.txt_ip.pack(side=tk.LEFT, padx=(0, 5))
        
        self.btn_connect = ttk.Button(ip_row, text="무선 연결", command=self.start_wireless_connect)
        self.btn_connect.pack(side=tk.RIGHT)
        
        # Auto Setup Row
        auto_row = ttk.Frame(wire_frame)
        auto_row.pack(fill=tk.X)
        
        self.btn_auto = ttk.Button(
            auto_row, 
            text="★ USB 기기로 무선 연결 자동 설정", 
            command=self.start_auto_setup
        )
        self.btn_auto.pack(fill=tk.X)
        
        # 3. Resolution Selection Frame
        res_frame = ttk.LabelFrame(self.main_frame, text=" 3. 해상도 및 화면 설정 ", padding="8")
        res_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.res_var = tk.StringVar(value="1280x720")
        self.cb_res = ttk.Combobox(
            res_frame, 
            textvariable=self.res_var, 
            values=["3840x2160", "2560x1440", "1920x1080", "1600x900", "1280x720", "960x540"], 
            state="readonly"
        )
        self.cb_res.pack(fill=tk.X)
        
        self.borderless_var = tk.BooleanVar(value=False)
        self.chk_borderless = ttk.Checkbutton(
            res_frame,
            text="테두리 없는 전체화면 (Borderless Fullscreen)",
            variable=self.borderless_var
        )
        self.chk_borderless.pack(fill=tk.X, pady=(5, 0))
        
        # 4. Launch Button
        self.btn_launch = tk.Button(
            self.main_frame,
            text="포켓몬 챔피언스 실행 (PC 독립 창)",
            font=("Malgun Gothic", 11, "bold"),
            bg="#4caf50",
            fg="white",
            relief=tk.RAISED,
            bd=1,
            command=self.launch_game
        )
        self.btn_launch.pack(fill=tk.X, ipady=8)
        
        # Status Label
        self.lbl_status = ttk.Label(self.main_frame, text="준비됨", font=("Malgun Gothic", 8), foreground="gray")
        self.lbl_status.pack(anchor=tk.W, pady=(5, 0))
        
        # Initial load
        self.refresh_devices()

    def set_status(self, text, color="gray"):
        self.lbl_status.config(text=text, foreground=color)
        self.root.update_idletasks()

    def refresh_devices(self):
        self.set_status("기기 목록 불러오는 중...", "blue")
        def run():
            stdout, stderr, code = run_cmd([ADB_PATH, "devices"])
            devices = []
            lines = stdout.splitlines()
            for line in lines:
                if "List of devices attached" in line or not line.strip():
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    devices.append(f"{parts[0]} ({parts[1]})")
            
            # Update UI in main thread
            self.root.after(0, lambda: self.update_device_list(devices))
            
        threading.Thread(target=run, daemon=True).start()

    def update_device_list(self, devices):
        self.cb_devices['values'] = devices
        if devices:
            self.cb_devices.current(0)
            self.set_status(f"기기 {len(devices)}대 감지됨", "green")
        else:
            self.dev_var.set("")
            self.set_status("감지된 기기 없음", "red")

    def start_wireless_connect(self):
        ip = self.txt_ip.get().strip()
        if not ip:
            messagebox.showerror("오류", "IP 주소를 입력해 주세요.")
            return
        
        self.set_status(f"무선 연결 시도 중 ({ip}:5555)...", "blue")
        self.btn_connect.config(state=tk.DISABLED)
        
        def run():
            stdout, stderr, code = run_cmd([ADB_PATH, "connect", f"{ip}:5555"])
            success = "connected to" in stdout.lower()
            
            def on_done():
                self.btn_connect.config(state=tk.NORMAL)
                if success:
                    messagebox.showinfo("무선 연결 성공", f"성공적으로 {ip}:5555에 연결되었습니다.")
                    self.set_status("무선 연결 성공", "green")
                else:
                    messagebox.showerror("무선 연결 실패", f"연결 실패:\n{stdout}\n{stderr}")
                    self.set_status("무선 연결 실패", "red")
                self.refresh_devices()
                
            self.root.after(0, on_done)
            
        threading.Thread(target=run, daemon=True).start()

    def start_auto_setup(self):
        self.set_status("자동 무선 설정 진행 중...", "blue")
        self.btn_auto.config(state=tk.DISABLED)
        
        def run():
            # 1. Find USB device
            stdout, stderr, code = run_cmd([ADB_PATH, "devices"])
            usb_device = None
            for line in stdout.splitlines():
                if "List of devices attached" in line or not line.strip():
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    dev_id = parts[0]
                    # USB devices typically do not contain IP address format
                    if ":" not in dev_id and "192.168" not in dev_id:
                        usb_device = dev_id
                        break
            
            if not usb_device:
                def err():
                    self.btn_auto.config(state=tk.NORMAL)
                    messagebox.showerror(
                        "오류", 
                        "USB로 연결된 스마트폰을 찾을 수 없습니다.\n먼저 폰을 USB로 연결해 주세요."
                    )
                    self.set_status("USB 기기 없음", "red")
                self.root.after(0, err)
                return
            
            # 2. Run adb tcpip 5555
            run_cmd([ADB_PATH, "-s", usb_device, "tcpip", "5555"])
            
            # 3. Get IP address of phone
            ip_stdout, ip_stderr, ip_code = run_cmd([ADB_PATH, "-s", usb_device, "shell", "ip route"])
            phone_ip = None
            # Find wlan0 IP src
            for line in ip_stdout.splitlines():
                if "wlan0" in line and "src" in line:
                    match = re.search(r"src\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
                    if match:
                        phone_ip = match.group(1)
                        break
            
            if not phone_ip:
                # Try fallback wlan0 ip addr show
                ip_stdout, _, _ = run_cmd([ADB_PATH, "-s", usb_device, "shell", "ip -o -4 addr show wlan0"])
                match = re.search(r"inet\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", ip_stdout)
                if match:
                    phone_ip = match.group(1)

            if not phone_ip:
                def err_ip():
                    self.btn_auto.config(state=tk.NORMAL)
                    messagebox.showerror(
                        "오류", 
                        "폰의 와이파이 IP 주소를 가져오지 못했습니다.\n폰이 와이파이에 연결되어 있는지 확인해 주세요."
                    )
                    self.set_status("IP 획득 실패", "red")
                self.root.after(0, err_ip)
                return

            # 4. Connect wirelessly
            run_cmd([ADB_PATH, "connect", f"{phone_ip}:5555"])
            
            def success_done():
                self.btn_auto.config(state=tk.NORMAL)
                self.txt_ip.delete(0, tk.END)
                self.txt_ip.insert(0, phone_ip)
                messagebox.showinfo(
                    "설정 완료", 
                    f"자동 설정이 완료되었습니다!\n무선 IP: {phone_ip}:5555\n\n이제 USB 케이블을 뽑으셔도 무선으로 조작 가능합니다."
                )
                self.set_status("자동 설정 성공", "green")
                self.refresh_devices()
                
            self.root.after(0, success_done)

        threading.Thread(target=run, daemon=True).start()

    def launch_game(self):
        selected = self.dev_var.get()
        if not selected:
            messagebox.showerror("오류", "연결된 기기가 없습니다. 새로고침을 하거나 무선 연결을 완료해 주세요.")
            return
        
        device_id = selected.split()[0]
        res = self.res_var.get()
        window_title = "Pokémon Champions"
        
        self.set_status("포켓몬 챔피언스 실행 및 미러링 시작...", "blue")
        
        # Hide the main Tkinter window immediately so it feels like it closed
        self.root.withdraw()
        
        def run_launch():
            # Wake up the phone display and dismiss the keyguard lock screen
            run_cmd([ADB_PATH, "-s", device_id, "shell", "input", "keyevent", "KEYCODE_WAKEUP"])
            run_cmd([ADB_PATH, "-s", device_id, "shell", "wm", "dismiss-keyguard"])
            
            # 1. Start App using monkey
            run_cmd([
                ADB_PATH, "-s", device_id, "shell", "monkey", 
                "-p", PKG_NAME, "-c", "android.intent.category.LAUNCHER", "1"
            ])
            
            # 2. Run scrcpy with custom window title and screen-off/stay-awake parameters
            scrcpy_args = [
                SCRCPY_PATH,
                "-s", device_id,
                f"--new-display={res}",
                f"--start-app={PKG_NAME}",
                "--no-vd-system-decorations",
                "--turn-screen-off",
                "--stay-awake",
                f"--window-title={window_title}"
            ]
            
            if self.borderless_var.get():
                scrcpy_args.extend(["--window-borderless", "--fullscreen"])
            
            try:
                # Launch scrcpy in background without CMD window
                subprocess.Popen(
                    scrcpy_args,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            except Exception as e:
                # If failed to launch, we need to show the window again to display error
                def err(msg):
                    self.root.deiconify()
                    messagebox.showerror("scrcpy 실행 오류", f"scrcpy 실행에 실패했습니다:\n{msg}")
                self.root.after(0, lambda: err(str(e)))
                return
            
            # 3. Wait for scrcpy window and set its icon dynamically
            icon_path = os.path.join(BASE_PATH, "bin", "scrcpy", "pokemon_icon.ico")
            if not os.path.exists(icon_path):
                icon_path = os.path.join(BASE_PATH, "pokemon_icon.ico")
                
            if os.path.exists(icon_path):
                try:
                    import time
                    import ctypes
                    
                    user32 = ctypes.windll.user32
                    WM_SETICON = 0x80
                    ICON_SMALL = 0
                    ICON_BIG = 1
                    IMAGE_ICON = 1
                    LR_LOADFROMFILE = 0x0010
                    
                    # Wait up to 12 seconds for the window to appear
                    hwnd = None
                    for _ in range(60):
                        time.sleep(0.2)
                        hwnd = user32.FindWindowW(None, window_title)
                        if hwnd:
                            break
                            
                    if hwnd:
                        # Load icon
                        h_icon = user32.LoadImageW(
                            None,
                            icon_path,
                            IMAGE_ICON,
                            0, 0,
                            LR_LOADFROMFILE
                        )
                        if h_icon:
                            user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, h_icon)
                            user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, h_icon)
                except Exception:
                    pass
            
            # Exit process cleanly
            import os as local_os
            local_os._exit(0)
            
        threading.Thread(target=run_launch, daemon=True).start()

# ----------------------------------------------------
# Main Execution
# ----------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    
    # Set Window Icon
    icon_path = os.path.join(BASE_PATH, "bin", "scrcpy", "pokemon_icon.ico")
    if not os.path.exists(icon_path):
        icon_path = os.path.join(BASE_PATH, "pokemon_icon.ico")
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception:
            pass
            
    app = AppLauncher(root)
    root.mainloop()
