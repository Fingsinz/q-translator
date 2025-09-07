import queue
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

import keyboard
import pyperclip
from PIL import Image, ImageDraw
from pystray import Icon
from pystray import MenuItem as item

from config import Config
from translator import APIS

gui_queue = queue.Queue()
config = Config()

class ResultWindow(tk.Toplevel):
    def __init__(self, text):
        super().__init__()
        self.title("翻译结果")
        self.geometry("500x300")
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)
        for api, enabled in Config().config["apis"].items():
            if enabled:
                frame = ttk.Frame(notebook)
                notebook.add(frame, text=api)
                txt = tk.Text(frame, wrap="word")
                txt.pack(fill="both", expand=True)
                txt.insert("1.0", APIS[api](text))
                txt.configure(state="disabled")

class SettingsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("设置")
        self.geometry("400x300")
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # 快捷键
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="快捷键")
        self.hk_var = tk.StringVar(value=Config().config["hotkey"])
        tk.Label(tab1, text="快捷键:").pack(pady=5)
        self.hk_entry = tk.Entry(tab1, textvariable=self.hk_var)
        self.hk_entry.pack(pady=5)
        tk.Button(tab1, text="录制快捷键", command=self.record_hotkey).pack(pady=5)

        # API
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="翻译API")
        self.api_vars = {}
        for api in APIS.keys():
            var = tk.BooleanVar(value=Config().config["apis"].get(api, False))
            chk = tk.Checkbutton(tab2, text=api, variable=var)
            chk.pack(anchor="w")
            self.api_vars[api] = var

        tk.Button(self, text="保存并应用", command=self.save_config).pack(pady=10)

    def record_hotkey(self):
        self.hk_var.set("（按组合键）")
        hotkey = keyboard.read_hotkey(suppress=False)
        self.hk_var.set(hotkey)

    def save_config(self):
        config = Config()
        config.config["hotkey"] = self.hk_var.get()
        for api, var in self.api_vars.items():
            config.config["apis"][api] = var.get()
        config.save()
        messagebox.showinfo("提示", "配置已保存！")

# ---------------- 热键 ----------------
def get_clipboard_text():
    keyboard.send("ctrl+c")
    time.sleep(0.05)
    return pyperclip.paste()

def hotkey_worker():
    def callback():
        config.load()  # 热加载
        text=get_clipboard_text()
        if text.strip(): gui_queue.put(("result", text))
    keyboard.add_hotkey(config.config["hotkey"], callback)
    keyboard.wait()

# ---------------- 托盘 ----------------
def create_icon():
    img=Image.new("RGB",(64,64),(255,255,255))
    d=ImageDraw.Draw(img)
    d.rectangle([16,16,48,48],fill=(0,0,0))
    return img

def on_quit(icon,item): icon.stop(); os._exit(0)
def on_settings(icon,item): gui_queue.put(("settings",None))

def tray_worker():
    icon=Icon("translator",create_icon(),menu=(
        item("设置",on_settings),
        item("退出",on_quit)
    ))
    icon.run()

# ---------------- 主线程 GUI 循环 ----------------
def gui_loop():
    root=tk.Tk()
    root.withdraw()
    def check_queue():
        try:
            while True:
                task,data=gui_queue.get_nowait()
                if task=="settings": SettingsWindow(root)
                elif task=="result": ResultWindow(data)
        except queue.Empty: pass
        root.after(100,check_queue)
    root.after(100,check_queue)
    root.mainloop()

# ---------------- 启动 ----------------
if __name__=="__main__":
    threading.Thread(target=hotkey_worker,daemon=True).start()
    threading.Thread(target=tray_worker,daemon=True).start()
    gui_loop()
