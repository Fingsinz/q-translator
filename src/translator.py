"""翻译器模块"""

import hashlib
import time

import requests

from config import Config

config = Config()


class YoudaoTranslator():
    """有道翻译器"""

    @staticmethod
    def translate(text, source_lang, target_lang):
        """翻译"""
        lang = {
            "自动": "auto",
            "英语": "en",
            "中文": "zh-CHS",
            "日语": "ja",
            "韩语": "ko",
            "法语": "fr",
            "德语": "de"
        }

        try:
            app_id = config.get_api_key("Youdao", "appID")
            secret_key = config.get_api_key("Youdao", "secretKey")
            if not app_id or not secret_key:
                return "[有道翻译错误] 未配置 API 密钥"

            data = {
                "q": text,
                "from": lang[source_lang],
                "to": lang[target_lang],
                "appKey": app_id,
                "salt": "123",
                "signType": "v3",
                "curtime": str(int(time.time())),
            }

            q_len = len(text)
            q = text if q_len < 20 else text[:10] + str(q_len) + text[-10:]

            data['sign'] = hashlib.sha256(
                (data['appKey'] + q + data['salt'] +
                 data['curtime'] + secret_key).encode("utf-8")
            ).hexdigest()

            response = requests.post(
                "https://openapi.youdao.com/api",
                data=data,
                timeout=5
            )

            response.raise_for_status()
            r_json = response.json()
            #print(response.json())

            if r_json["errorCode"] != "0":
                return "[有道翻译错误] " + r_json["errorCode"]

            return r_json["translation"][0]
        except Exception as e:  # pylint: disable=broad-except
            return f"[有道翻译错误] {str(e)}"

class BaiduTranslator():
    """百度翻译器"""

    @staticmethod
    def translate(text, source_lang, target_lang):
        """翻译"""
        lang = {
            "自动": "auto",
            "英语": "en",
            "中文": "zh",
            "日语": "jp",
            "韩语": 'kor',
            "法语": "fra",
            "德语": "de"
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
                (data['appid'] + text + data['salt'] + secret_key).encode("utf-8")
            ).hexdigest()

            response = requests.post(
                "https://fanyi-api.baidu.com/api/trans/vip/translate",
                data=data,
                timeout=5
            )

            response.raise_for_status()
            r_json = response.json()
            #print(r_json)

            if r_json.get("error_code"):
                return "[百度翻译错误] " + r_json["error_code"]

            return_str = ""
            for result in r_json["trans_result"]:
                return_str += result["dst"] + "\n"
            return return_str

        except Exception as e:  # pylint: disable=broad-except
            return f"[百度翻译错误] {str(e)}"

APIS = {
    "Youdao": YoudaoTranslator(),
    "Baidu": BaiduTranslator()
}
