"""工具模块"""

import re  # pylint: disable=unused-import


def check_zh(text):
    """判断是否包含中文"""
    return bool(re.search('[\u4e00-\u9fa5]', text))
