"""主模块"""

# 标准库导入
import os
import queue
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

# 第三方库导入
import keyboard
import pyperclip
from PIL import Image, ImageDraw
from pystray import Icon
from pystray import MenuItem as item

# 本地模块导入
from config import Config
from translator import APIS
from utils import check_zh

# 全局变量
gui_queue = queue.Queue()
config = Config()
supported_lang = ["自动", "英语", "中文", "日语", "韩语", "法语", "德语"]

# ---------------- GUI ----------------
class ResultWindow(tk.Toplevel):
    """结果窗口"""
    def __init__(self, text):
        super().__init__()
        self.mapping = {
            "Google": "谷歌翻译",
            "DeepL": "DeepL翻译",
            "Youdao": "有道翻译",
            "Baidu": "百度翻译"
        }
        self.d_mapping = {
            "谷歌翻译": "Google",
            "DeepL翻译": "DeepL",
            "有道翻译": "Youdao",
            "百度翻译": "Baidu"
        }

        self.history = {}
        self.tabs = {}

        self.title("翻译结果")
        # 获取鼠标当前位置并设置窗口位置
        x = self.winfo_pointerx()
        y = self.winfo_pointery()
        self.geometry(f"500x400+{x}+{y}")

        # 语言选择区域
        lang_frame = ttk.Frame(self)
        lang_frame.pack(fill="x", padx=5, pady=5)

        # 源语言选择
        tk.Label(lang_frame, text="源语言:").pack(side="left")
        self.source_lang = ttk.Combobox(lang_frame,
                                        values=supported_lang,
                                        state="readonly")
        self.source_lang.pack(side="left", padx=5)

        # 目标语言选择
        tk.Label(lang_frame, text="目标语言:").pack(side="left")
        self.target_lang = ttk.Combobox(lang_frame,
                                        values=supported_lang[1:],
                                        state="readonly")
        self.target_lang.pack(side="left", padx=5)

        is_zh = check_zh(text)
        if is_zh:
            self.source_lang.set("中文")
            self.target_lang.set("英语")
        else:
            self.source_lang.set("自动")
            self.target_lang.set("中文")

        # 添加“复制并关闭”按钮
        button_frame = ttk.Frame(lang_frame)
        button_frame.pack(fill="x", padx=5, pady=5)

        copy_button = ttk.Button(
            button_frame,
            text="复制并关闭",
            command=self.copy_and_close
        )
        copy_button.pack(side="right", padx=5)

        # 翻译结果显示区域
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)
        self.notebook = notebook
        self.text = text

        # API 选择
        for api, info in config.config["apis"].items():
            enabled = info.get("enable", False)
            if enabled:
                frame = ttk.Frame(self.notebook)
                self.notebook.add(frame, text=self.mapping[api])
                txt = tk.Text(frame, wrap="word", font=("微软雅黑", 16))
                txt.pack(fill="both", expand=True)
                self.tabs[api] = frame

        # 初始化翻译结果
        self.notebook.bind("<<NotebookTabChanged>>",
                           lambda event: self.update_translation(
                               api=self.notebook.tab(self.notebook.select(), "text"),
                               text=self.text
                            ))
        self.target_lang.bind("<<ComboboxSelected>>",
                              lambda event: self.update_translation(
                                  api=self.notebook.tab(self.notebook.select(), "text"),
                                  text=self.text
                               ))

        #self.update_translation(api=self.notebook.tab(self.notebook.select(), "text"),
        #                        text=self.text)

    def update_translation(self, api, text):
        """更新翻译"""
        api = self.d_mapping[api]

        # 清除当前api的翻译结果
        now_tab = self.tabs[api]
        txt = now_tab.winfo_children()[0]
        txt.delete("1.0", "end")

        # 获取选择的语言对
        source_lang = self.source_lang.get()
        target_lang = self.target_lang.get()

        # 更新翻译结果
        if self.history.get(api):
            if self.history[api][0] == source_lang and self.history[api][1] == target_lang:
                #print("Use history")
                txt.insert("1.0", self.history[api][2])
                return

        #print("Use API")
        translator = APIS[api]
        result = translator.translate(text, source_lang, target_lang)
        self.history[api] = (source_lang, target_lang, result)

        txt.insert("1.0", result)

    def copy_and_close(self):
        """复制当前翻译结果并关闭窗口"""
        api = self.d_mapping[self.notebook.tab(self.notebook.select(), "text")]
        now_tab = self.tabs[api]
        txt = now_tab.winfo_children()[0]
        text = txt.get("1.0", "end")
        text = text.strip()

        # 复制到剪贴板
        pyperclip.copy(text)
        self.destroy()


class SettingsWindow(tk.Toplevel):
    """设置窗口"""
    def __init__(self, master):
        super().__init__(master)
        self.title("设置")
        self.geometry("400x300")
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # 快捷键
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="快捷键")
        self.hk_var = tk.StringVar(value=config.config["hotkey"])
        tk.Label(tab1,text="快捷键:").pack(pady=5)

        self.hk_entry = tk.Entry(tab1,textvariable=self.hk_var)
        self.hk_entry.pack(pady=5)
        tk.Button(tab1,text="录制快捷键",command=self.record_hotkey).pack(pady=5)

        # API
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="翻译API")
        self.api_vars = {}

        api_name = APIS.keys()
        for api in api_name:
            var = tk.BooleanVar(value=str(config.config["apis"].get(api, {}).get("enable", False)))
            chk = tk.Checkbutton(tab2,text=api,variable=var)
            chk.pack(anchor="w")
            self.api_vars[api] = var

        tk.Button(self,text="保存并应用",command=self.save_config).pack(pady=10)

    def record_hotkey(self):
        """录制快捷键"""
        self.hk_var.set("（按组合键）")
        hotkey = keyboard.read_hotkey(suppress=False)
        self.hk_var.set(hotkey)

    def save_config(self):
        """保存配置"""
        config.config["hotkey"] = self.hk_var.get()
        for api, var in self.api_vars.items():
            config.config["apis"][api] = var.get()
        config.save()
        messagebox.showinfo("提示","配置已保存！")

# ---------------- 热键 ----------------
def get_clipboard_text():
    """获取剪贴板文本"""
    keyboard.send("ctrl+c")
    time.sleep(0.05)
    return pyperclip.paste()

def hotkey_worker():
    """响应快捷键"""
    def callback():
        config.load()  # 热加载
        text = get_clipboard_text()
        if text.strip():
            gui_queue.put(("result", text))
    keyboard.add_hotkey(config.config["hotkey"], callback)
    keyboard.wait()

# ---------------- 托盘 ----------------
def create_icon():
    """图标创建"""
    img = Image.new("RGB", (64,64), (255,255,255))
    d = ImageDraw.Draw(img)
    d.rectangle([12, 16, 56, 20], fill=(0,0,0))
    d.rectangle([32, 24, 36, 56], fill=(0,0,0))
    img.save("./icon.ico")
    return img

def on_quit(icon, item):    # pylint: disable=unused-argument, disable=redefined-outer-name
    """退出程序"""
    icon.stop()
    os._exit(0)

def on_settings(icon, item):    # pylint: disable=unused-argument, disable=redefined-outer-name
    """响应设置页面"""
    gui_queue.put(("settings",None))

def tray_worker():
    """启动托盘"""
    icon_path = "./icon.ico"
    if not os.path.exists(icon_path):
        icon_img = create_icon()
    else:
        icon_img = Image.open(icon_path)

    icon = Icon("translator",
                icon_img,
                menu=(item("设置",on_settings),
                      item("退出",on_quit)
                )
    )
    icon.run()

# ---------------- 主线程 GUI 循环 ----------------
def gui_loop():
    """主线程循环"""
    root = tk.Tk()
    root.withdraw()
    def check_queue():
        try:
            while True:
                task, data = gui_queue.get_nowait()
                if task == "settings":
                    SettingsWindow(root)
                elif task == "result":
                    ResultWindow(data)
        except queue.Empty:
            pass
        root.after(100,check_queue)
    root.after(100,check_queue)
    root.mainloop()

# ---------------- 启动 ----------------
if __name__=="__main__":
    threading.Thread(target=hotkey_worker,daemon=True).start()
    threading.Thread(target=tray_worker,daemon=True).start()
    gui_loop()
