# Q-Translator (Quick Translator)

*Assisted by Tencent Cloud CodeBuddy and ChatGPT*

## Introduction 介绍

Q-Translator 是一个用于快速翻译的软件, 按下快捷键即调用翻译 API 的工具.

起因是找不到 (懒得找) 类似地划词翻译软件, 于是就自己结合 AI 写了一个.

## Install 安装

### 从源码编译

使用 uv 同步环境:

```bash
uv venv
uv sync
```

运行程序:

```bash
cd src
uv run main.py
```

打包:

```bash
pyinstaller -F -w main.py --icon=icon.ico
```

### 下载二进制文件

[Releases](https://github.com/Fingsinz/q-translator/releases)

解压后打开 .exe 即可，程序运行在后台.

## Usage 使用

0. 申请相关翻译的 Key, 并设置在配置文件 `config.json` 中;
1. 鼠标光标选中文本;
2. 按下快捷键 (并复制文本);
3. 弹出窗口，源语言默认为 `auto`, 设置目标语言后自动调用 API 翻译.

*实际上, 即使鼠标没有选中文本, 程序也会自动翻译粘贴板最新的文本.*

## 功能

- [x] 百度翻译 API, 支持中文, 英语, 日语, 韩语, 法语, 德语间互译.
- [ ] 有道翻译 API, 支持中文, 英语, 日语, 韩语, 法语, 德语间互译.
- [ ] 谷歌翻译 API, 支持中文, 英语, 日语, 韩语, 法语, 德语间互译.
- [ ] 腾讯翻译 API, 支持中文, 英语, 日语, 韩语, 法语, 德语间互译.
- [ ] 必应翻译 API, 支持中文, 英语, 日语, 韩语, 法语, 德语间互译.

未来加上的功能:

- [ ] 复制并关闭窗口
- [ ] 自适应中英翻译
