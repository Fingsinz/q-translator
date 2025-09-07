import json
import os

CONFIG_FILE = "config.json"

class Config:
    default = {
        "hotkey": "ctrl+shift+t",
        "apis": {"Google": True, "DeepL": False, "Youdao": False, "Baidu": False}
    }

    def __init__(self):
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.default, f, indent=4)
        self.load()

    def load(self):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def save(self):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)