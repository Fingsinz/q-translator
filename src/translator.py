import hashlib

import requests

from config import Config

config = Config()

class GoogleTranslator:
    """谷歌翻译器"""
    def __init__(self):
        self.lang = {
            "auto": "auto",
            "en": "en",
            "zh": "zh-CN",
            "ja": "ja",
            "ko": "ko",
            "fr": "fr",
            "de": "de"
        }

    def translate(self, text, source_lang="auto", target_lang="zh"):
        """翻译"""

        try:
            api_key = config.get_api_key("Google", "key")
            if not api_key:
                return "[Google翻译错误] 未配置 API 密钥"

            params = {
                "key": api_key,
                "q": text,
                "source": source_lang,
                "target": target_lang
            }

            response = requests.post(
                "https://translation.googleapis.com/language/translate/v2",
                params=params,
                timeout=5
            )

            response.raise_for_status()
            return response.json()["data"]["translations"][0]["translatedText"]
        except Exception as e:  # pylint: disable=broad-except
            return f"[Google翻译错误] {str(e)}"

class DeeplTranslator:
    """DeepL翻译器"""
    def __init__(self):
        self.lang = {
            "auto": "auto",
            "en": "EN",
            "zh": "ZH",
            "ja": "JA",
            "ko": "KO",
            "fr": "FR",
            "de": "DE"
        }

    def translate(self, text, target_lang="ZH"):
        """翻译"""
        try:
            auth_key = config.get_api_key("DeepL", "auth_key")
            if not auth_key:
                return "[DeepL翻译错误] 未配置 API 密钥"

            data = {
                "auth_key": auth_key,
                "text": text,
                "target_lang": target_lang
            }

            response = requests.post(
                "https://api.deepl.com/v2/translate",
                data=data,
                timeout=5
            )

            response.raise_for_status()
            return response.json()["translations"][0]["text"]
        except Exception as e:  # pylint: disable=broad-except
            return f"[DeepL翻译错误] {str(e)}"

class YoudaoTranslator():
    """有道翻译器"""
    def __init__(self):
        self.lang = {
            "auto": "auto",
            "en": "en",
            "zh": "zh-CHS",
            "ja": "ja",
            "ko": "ko",
            "fr": "fr",
            "de": "de"
        }
    def translate(self, text, source_lang="auto", target_lang="zh"):
        """翻译"""
        try:
            app_id = config.get_api_key("Youdao", "appID")
            secret_key = config.get_api_key("Youdao", "secretKey")
            if not app_id or not secret_key:
                return "[有道翻译错误] 未配置 API 密钥"

            data = {
                "q": text,
                "from": source_lang,
                "to": target_lang,
                "appKey": app_id,
                "secretKey": secret_key
            }

            response = requests.post(
                "https://openapi.youdao.com/api",
                data=data,
                timeout=5
            )

            response.raise_for_status()
            return response.json()["translation"][0]
        except Exception as e:  # pylint: disable=broad-except
            return f"[有道翻译错误] {str(e)}"

class BaiduTranslator():
    """百度翻译器"""
    @staticmethod
    def translate(text, source_lang="auto", target_lang="zh"):
        """翻译"""
        lang = {
            "auto": "auto",
            "en": "en",
            "zh": "zh",
            "ja": "jp",
            "ko": 'kor',
            "fr": "fra",
            "de": "de"
        }

        try:
            app_id = config.get_api_key("Baidu", "appID")
            secret_key = config.get_api_key("Baidu", "secretKey")
            if not app_id or not secret_key:
                return "[百度翻译错误] 未配置 API 密钥"

            data = {
                "q": text,
                "from": lang[source_lang],
                "to": lang[target_lang],
                "appid": app_id,
                "salt": "123",
            }

            data['sign'] = hashlib.md5(
                (data['appid'] + text + data['salt'] + secret_key).encode()
            ).hexdigest()

            response = requests.post(
                "https://fanyi-api.baidu.com/api/trans/vip/translate",
                data=data,
                timeout=5
            )

            response.raise_for_status()
            print(response.json())
            return response.json()["trans_result"][0]["dst"]
        except Exception as e:  # pylint: disable=broad-except
            return f"[百度翻译错误] {str(e)}"

APIS = {
    "Google": GoogleTranslator(),
    "DeepL": DeeplTranslator(),
    "Youdao": YoudaoTranslator(),
    "Baidu": BaiduTranslator().translate
}
