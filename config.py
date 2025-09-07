import json
import os

CONFIG_FILE = "config.json"

class Config:
    """配置管理类"""
    default = {
        "hotkey": "ctrl+shift+t",
        "apis": {
            "Google": {
                "enable": True,
                "key": "YOUR_GOOGLE_API_KEY"
            },

            "DeepL": {
                "enable": True,
                "auth_key": "YOUR_DEEPL_API_KEY"
            },

            "Youdao": {
                "enable": True,
                "appKey": "YOUR_YOUDAO_API_KEY",
                "secretKey": "YOUR_YOUDAO_SECRET_KEY"
            },

            "Baidu": {
                "enable": True,
                "appKey": "YOUR_BAIDU_API_KEY",
                "secretKey": "YOUR_BAIDU_SECRET_KEY"
            }
        }
    }

    def __init__(self):
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.default, f, indent=4)
        self.load()

    def load(self):
        """加载配置文件"""
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def save(self):
        """写入配置文件"""
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    def get_api_key(self, api_name, key_type="key"):
        """
        获取指定 API 的密钥
        :param api_name: API 名称（如 "Google"）
        :param key_type: 密钥类型（如 "key", "auth_key", "appKey"）
        :return: 密钥值，如果未找到则返回 None
        """
        api_config = self.config["apis"].get(api_name, {})
        return api_config.get(key_type)
