# Урок 4: Функции и работа с файлами

# --- 1. Определяем функцию (def) ---
def greet(name):
    """Возвращает приветствие для указанного имени."""
    return f"Привет, {name}! Добро пожаловать в Python."

def save_note(filename, content):
    """Сохраняет заметку в файл."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Заметка сохранена в файл: {filename}")

def read_note(filename):
    """Читает и возвращает содержимое файла."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None

# --- 2. Используем функции ---

# Приветствие
user_name = input("Как тебя зовут? ")
message = greet(user_name)
print(message)

# Работа с заметками
print("\n📝 Создадим заметку.")
note_text = input("Напиши что-нибудь: ")
note_file = "my_note.txt"
save_note(note_file, note_text)

print("\n📖 Читаем сохранённую заметку:")
saved_text = read_note(note_file)
if saved_text:
    print("-" * 30)
    print(saved_text)
    print("-" * 30)
else:
    print("❌ Не удалось прочитать файл.")