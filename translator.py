def google_translate(text): return f"[Google翻译] {text}"
def deepl_translate(text): return f"[DeepL翻译] {text}"
def youdao_translate(text): return f"[有道翻译] {text}"
def baidu_translate(text): return f"[百度翻译] {text}"

APIS = {"Google": google_translate, "DeepL": deepl_translate,
        "Youdao": youdao_translate, "Baidu": baidu_translate}