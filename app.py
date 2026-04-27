import asyncio
import os
import tempfile
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from gigachat import GigaChat
from prometheus_client import start_http_server, Counter
import fitz  # PyMuPDF

# --- НАСТРОЙКИ ---
TOKEN = os.environ.get("TOKEN", "8635674583:AAGstQqoxW4u6vl_XSJLgbkB2zsgY953O_0")
GIGACHAT_KEY = os.environ.get("GIGACHAT_KEY", "MDE5ZGExZDctMzU3Ni03ODBhLWI5NTItOTc0NjlmY2E5YmNmOjQ4ZDk1MDg3LTE2NTktNGUyNi1iNWVjLTNkZDYxMjJlMzIwNw==")
client = GigaChat(credentials=GIGACHAT_KEY, verify_ssl_certs=False)

DEFAULT_MODEL = "GigaChat"
MAX_HISTORY = 10
LOG_FILE = "/data/bot_log.txt"
MAX_MESSAGE_LENGTH = 4096

user_data = {}
last_interaction = {}
pdf_storage = {}  # {user_id: [{"file_name": "...", "text": "..."}]}

# --- Метрики ---
MESSAGES_RECEIVED = Counter('bot_messages_received', 'Total messages received')
ERRORS_TOTAL = Counter('bot_errors_total', 'Total errors')
COMMANDS_TOTAL = Counter('bot_commands_total', 'Total commands', ['command'])

# --- Вспомогательные функции ---
def log_message(user_info: str, message_type: str, content: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {user_info} | {message_type}: {content}\n"
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)
    print(log_line.strip())

def split_long_message(text: str, max_len: int = MAX_MESSAGE_LENGTH) -> list:
    if len(text) <= max_len:
        return [text]
    parts = []
    while text:
        if len(text) <= max_len:
            parts.append(text)
            break
        split_at = text.rfind("\n", 0, max_len)
        if split_at == -1:
            split_at = text.rfind(" ", 0, max_len)
        if split_at == -1:
            split_at = max_len
        parts.append(text[:split_at].strip())
        text = text[split_at:].lstrip()
    return parts

async def send_with_retry(update: Update, text: str, reply_markup=None, max_retries: int = 3):
    if update.message is None and update.callback_query is None:
        return
    target = update.message if update.message else update.callback_query.message
    for attempt in range(max_retries):
        try:
            return await target.reply_text(text, reply_markup=reply_markup)
        except Exception as e:
            error_str = str(e)
            if ("503" in error_str or "ReadError" in error_str) and attempt < max_retries - 1:
                await asyncio.sleep(3)
            else:
                raise e

def get_buttons():
    keyboard = [
        [
            InlineKeyboardButton("🔄 Перегенерировать", callback_data="regenerate"),
            InlineKeyboardButton("🗑️ Удалить", callback_data="delete"),
        ],
        [
            InlineKeyboardButton("👍", callback_data="rate_good"),
            InlineKeyboardButton("👎", callback_data="rate_bad"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- Команды бота ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    COMMANDS_TOTAL.labels(command='start').inc()
    user = update.effective_user
    user_info = f"{user.full_name} (@{user.username}) [{user.id}]"
    log_message(user_info, "COMMAND", "/start")
    await send_with_retry(update,
        "🤖 Привет! Я ИИ-ассистент с RAG.\n\n"
        "Команды:\n"
        "/help — список команд\n"
        "/reset — сбросить историю\n"
        "/ask <вопрос> — спросить по PDF\n"
        "/list — показать загруженные PDF\n\n"
        "Отправь мне PDF, DOCX или TXT файл, и я его запомню!"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    COMMANDS_TOTAL.labels(command='help').inc()
    user = update.effective_user
    user_info = f"{user.full_name} (@{user.username}) [{user.id}]"
    log_message(user_info, "COMMAND", "/help")
    await send_with_retry(update,
        "📋 Доступные команды:\n"
        "/start — приветствие\n"
        "/help — это сообщение\n"
        "/reset — сбросить историю\n"
        "/ask <вопрос> — спросить по загруженным PDF\n"
        "/list — показать загруженные файлы\n\n"
        "Отправь мне PDF-файл, и я его запомню!"
    )

async def set_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    await send_with_retry(update, "ℹ️ Бот использует облачную модель GigaChat. Смена модели отключена.")

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    user_id = update.effective_user.id
    user = update.effective_user
    user_info = f"{user.full_name} (@{user.username}) [{user.id}]"
    log_message(user_info, "COMMAND", "/reset")
    if user_id in user_data:
        user_data[user_id]["history"] = []
    if user_id in last_interaction:
        del last_interaction[user_id]
    await send_with_retry(update, "🧹 История сброшена.")

# --- RAG: обработка документов (PDF, DOCX, TXT) ---
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if not document:
        return

    file_name = document.file_name.lower()
    user_id = update.effective_user.id

    # Проверяем поддерживаемые форматы
    if not (file_name.endswith('.pdf') or file_name.endswith('.docx') or file_name.endswith('.txt')):
        await update.message.reply_text("❌ Поддерживаются только PDF, DOCX и TXT файлы.")
        return

    await update.message.reply_text("⏳ Обрабатываю документ...")

    file = await context.bot.get_file(document.file_id)
    full_text = ""

    with tempfile.NamedTemporaryFile(delete=False, suffix='.' + file_name.split('.')[-1]) as tmp:
        await file.download_to_drive(tmp.name)

        try:
            if file_name.endswith('.pdf'):
                # PDF
                doc = fitz.open(tmp.name)
                for page in doc:
                    full_text += page.get_text()
                doc.close()

            elif file_name.endswith('.docx'):
                # Word
                from docx import Document
                doc = Document(tmp.name)
                for para in doc.paragraphs:
                    full_text += para.text + '\n'

            elif file_name.endswith('.txt'):
                # TXT
                with open(tmp.name, 'r', encoding='utf-8', errors='replace') as f:
                    full_text = f.read()

        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при чтении файла: {e}")
            return

    if not full_text.strip():
        await update.message.reply_text("❌ Не удалось извлечь текст из документа.")
        return

    if user_id not in pdf_storage:
        pdf_storage[user_id] = []
    pdf_storage[user_id].append({
        "file_name": document.file_name,
        "text": full_text
    })

    await update.message.reply_text(f"✅ Документ обработан! Всего файлов: {len(pdf_storage[user_id])}")

# --- RAG: команда /ask ---
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    user_id = update.effective_user.id
    question = ' '.join(context.args) if context.args else None

    if not question:
        await update.message.reply_text("❌ Напиши вопрос после /ask. Например: /ask О чём документ?")
        return

    if user_id not in pdf_storage or not pdf_storage[user_id]:
        await update.message.reply_text("❌ У вас нет загруженных PDF. Сначала отправьте файл.")
        return

    await update.message.reply_text("🔍 Ищу ответ в документах...")

    all_texts = [item['text'] for item in pdf_storage[user_id]]
    combined = "\n\n".join(all_texts)
    if len(combined) > 3000:
        combined = combined[:3000] + "..."

    try:
        # Экранируем кириллицу через repr, чтобы избежать проблем с кодировкой
        safe_question = repr(question)
        safe_combined = repr(combined)

        prompt = (
            f"Context: {safe_combined}\n\n"
            f"Question: {safe_question}\n\n"
            "Answer the question based on the context. Answer in Russian."
        )
        response = client.chat({"messages": [{"role": "user", "content": prompt}]})
        answer = response.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при поиске: {e}")

# --- RAG: команда /list ---
async def list_docs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in pdf_storage or not pdf_storage[user_id]:
        await update.message.reply_text("📂 У вас нет загруженных PDF.")
        return
    names = [item['file_name'] for item in pdf_storage[user_id]]
    await update.message.reply_text("📂 Загруженные файлы:\n" + "\n".join(f"- {n}" for n in names))

# --- Обработка обычных сообщений (чат) ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return
    MESSAGES_RECEIVED.inc()
    user_id = update.effective_user.id
    user = update.effective_user
    user_info = f"{user.full_name} (@{user.username}) [{user.id}]"
    user_message = update.message.text

    log_message(user_info, "USER", user_message)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    if user_id not in user_data:
        user_data[user_id] = {"history": [], "model": DEFAULT_MODEL}

    history = user_data[user_id]["history"]
    history.append({"role": "user", "content": user_message})

    try:
        response = client.chat({"messages": history})
        reply = response.choices[0].message.content
        log_message(user_info, "BOT", reply[:100] + "..." if len(reply) > 100 else reply)
    except Exception as e:
        ERRORS_TOTAL.inc()
        reply = f"❌ Ошибка GigaChat: {e}"
        log_message(user_info, "ERROR", str(e))
        history.pop()
        await send_with_retry(update, reply)
        return
    else:
        history.append({"role": "assistant", "content": reply})

    if len(history) > MAX_HISTORY * 2:
        user_data[user_id]["history"] = history[-(MAX_HISTORY * 2):]

    last_interaction[user_id] = {"prompt": user_message, "reply": reply}

    for part in split_long_message(reply):
        await send_with_retry(update, part, reply_markup=get_buttons())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user = query.from_user
    user_info = f"{user.full_name} (@{user.username}) [{user.id}]"

    if query.data == "delete":
        await query.message.delete()
        log_message(user_info, "BUTTON", "Удалить сообщение")
        return

    if query.data == "rate_good":
        await query.answer("Спасибо за оценку! 👍")
        log_message(user_info, "RATING", "👍")
        return

    if query.data == "rate_bad":
        await query.answer("Жаль, что ответ не понравился 😔")
        log_message(user_info, "RATING", "👎")
        return

    if query.data == "regenerate":
        log_message(user_info, "BUTTON", "Перегенерировать")
        if user_id not in last_interaction:
            await query.edit_message_text("❌ Нечего перегенерировать.")
            return

        prompt = last_interaction[user_id]["prompt"]
        await query.edit_message_text(f"🔄 Перегенерирую ответ на: \"{prompt}\"...")

        if user_id not in user_data:
            user_data[user_id] = {"history": [], "model": DEFAULT_MODEL}

        history = user_data[user_id]["history"]
        if history and history[-1]["role"] == "assistant":
            history.pop()

        try:
            response = client.chat({"messages": history})
            new_reply = response.choices[0].message.content
        except Exception as e:
            ERRORS_TOTAL.inc()
            new_reply = f"❌ Ошибка GigaChat: {e}"
        else:
            history.append({"role": "assistant", "content": new_reply})
            last_interaction[user_id]["reply"] = new_reply

        await query.edit_message_text(new_reply, reply_markup=get_buttons())

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("model", set_model))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("list", list_docs))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    start_http_server(8000)
    print(f"🤖 Бот запущен на GigaChat с RAG. Метрики: :8000")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()