import openai
import locale

GPT_ENABLED = True # Set to False to disable AI-powered analysis
OPENAI_API_KEY = "your_openai_api_key"
openai.api_key = OPENAI_API_KEY

LANG = locale.getdefaultlocale()[0]  # for example 'ru_RU' или 'en_US'

def ask_gpt_about_file(path: str, size_bytes: int) -> str:
    size_mb = round(size_bytes / (1024**2), 2)

    if LANG.startswith("ru"):
        prompt = f"""
Файл: {path}
Размер: {size_mb} МБ

Можно ли удалить этот файл без вреда для системы или приложений?
Ответь 'Да' или 'Нет' и кратко объясни.
"""
    else:
        prompt = f"""
File: {path}
Size: {size_mb} MB

Can this file be safely deleted without harming the system or apps?
Reply 'Yes' or 'No' and briefly explain.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[GPT ERROR] {e}"
