import locale
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

GPT_ENABLED = True # Set to False to disable AI-powered analysis
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

LANG = locale.getdefaultlocale()[0]

def ask_gpt_about_file(path: str, size_bytes: int) -> str:
    size_mb = round(size_bytes / (1024**2), 2)

    if LANG.startswith("ru"):
        prompt = f"""
Файл: {path}
Размер: {size_mb} МБ

Можно ли удалить этот файл без вреда для системы или приложений?
Либо же можно ли удалить некоторые содержимые этого файла или папки?
Ответь 'Да' или 'Нет' и кратко объясни.
"""
    else:
        prompt = f"""
File: {path}
Size: {size_mb} MB

Can this file be safely deleted without harming the system or apps?
Alternatively, is it possible to delete some of the contents of this file or folder?
Reply 'Yes' or 'No' and briefly explain.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[GPT ERROR] {e}"
