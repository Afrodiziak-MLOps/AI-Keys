import subprocess
import sys
import time

MODEL_NAME = "llama3.2:3b"
TEST_RETRIES = 3
RETRY_DELAY_SEC = 5

def run_command(cmd):
    """Выполняет команду в терминале и возвращает результат."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def is_model_installed(model_name):
    """Проверяет, установлена ли модель в Ollama."""
    stdout, stderr, code = run_command("ollama list")
    if code != 0:
        print(f"❌ Ошибка при проверке моделей: {stderr}")
        return False
    return model_name in stdout

def pull_model(model_name):
    """Скачивает модель из реестра Ollama."""
    print(f"⏳ Модель '{model_name}' не найдена. Начинаю загрузку...")
    stdout, stderr, code = run_command(f"ollama pull {model_name}")

    if code == 0:
        print(f"✅ Модель '{model_name}' успешно загружена.")
        return True
    else:
        print(f"❌ Ошибка при загрузке модели: {stderr}")
        return False

def test_model(model_name, retries=TEST_RETRIES, delay=RETRY_DELAY_SEC):
    """Отправляет тестовый запрос с повторными попытками."""
    import ollama
    for attempt in range(1, retries + 1):
        print(f"🧪 Попытка {attempt} из {retries}...")
        try:
            response = ollama.chat(
                model=model_name,
                messages=[{"role": "user", "content": "Привет, мир!"}]
            )
            reply_preview = response['message']['content'][:50]
            print(f"✅ Тест пройден. Ответ: {reply_preview}...")
            return True
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
            if attempt < retries:
                print(f"⏳ Жду {delay} сек перед повтором...")
                time.sleep(delay)
            else:
                print(f"❌ Все попытки исчерпаны.")
                return False

if __name__ == "__main__":
    print(f"🚀 Запуск деплоймента модели '{MODEL_NAME}'")

    if not is_model_installed(MODEL_NAME):
        if not pull_model(MODEL_NAME):
            sys.exit(1)
    else:
        print(f"✅ Модель '{MODEL_NAME}' уже установлена.")

    if test_model(MODEL_NAME):
        print(f"🎉 Деплоймент модели '{MODEL_NAME}' завершён успешно.")
    else:
        print(f"💥 Деплоймент модели '{MODEL_NAME}' провален.")
        sys.exit(1)