import openai

GPT_ENABLED = True # Set to False to disable AI-powered analysis
OPENAI_API_KEY = "your_openai_api_key"
openai.api_key = OPENAI_API_KEY

def ask_gpt_about_file(path: str, size_bytes: int) -> str:
    prompt = f"""
Файл: {path}
Размер: {round(size_bytes / (1024**2), 2)} МБ

Можно ли удалить этот файл без вреда для системы или приложений?
Ответь 'Да' или 'Нет' и кратко объясни.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[GPT ERROR] {e}"
