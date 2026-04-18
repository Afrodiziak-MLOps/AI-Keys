import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import ollama
from datetime import datetime

# --- НАСТРОЙКИ ---
TOKEN = "8635674583:AAGstQqoxW4u6vl_XSJLgbkB2zsgY953O_0"  # ← ЗАМЕНИТЕ
DEFAULT_MODEL = "llama3.2:3b"
MAX_HISTORY = 10
LOG_FILE = "bot_log.txt"
MAX_MESSAGE_LENGTH = 4096

user_data = {}
last_interaction = {}

# --- Вспомогательные функции ---
def log_message(user_info: str, message_type: str, content: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {user_info} | {message_type}: {content}\n"
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
    user = update.effective_user
    user_info = f"{user.full_name} (@{user.username}) [{user.id}]"
    log_message(user_info, "COMMAND", "/start")
    await send_with_retry(update,
        "🤖 Привет! Я ИИ-ассистент.\n"
        f"Текущая модель: {DEFAULT_MODEL}\n\n"
        "Команды:\n"
        "/help — список команд\n"
        "/model <имя> — сменить модель\n"
        "/reset — сбросить историю"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    user = update.effective_user
    user_info = f"{user.full_name} (@{user.username}) [{user.id}]"
    log_message(user_info, "COMMAND", "/help")
    await send_with_retry(update,
        "📋 Доступные команды:\n"
        "/start — приветствие\n"
        "/help — это сообщение\n"
        "/model <имя> — сменить модель\n"
        "/reset — сбросить историю"
    )

async def set_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    user_id = update.effective_user.id
    user = update.effective_user
    user_info = f"{user.full_name} (@{user.username}) [{user.id}]"

    if not context.args:
        await send_with_retry(update, "❌ Укажите модель. Пример: /model tinyllama")
        return

    model_name = context.args[0]
    try:
        models = ollama.list()
        available = [m["name"] for m in models["models"]]
        if model_name not in available:
            await send_with_retry(update, f"❌ Модель '{model_name}' не найдена.\nДоступные: {', '.join(available)}")
            return
    except:
        pass

    if user_id not in user_data:
        user_data[user_id] = {"history": [], "model": DEFAULT_MODEL}
    user_data[user_id]["model"] = model_name
    await send_with_retry(update, f"✅ Модель изменена на: {model_name}")

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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return
    user_id = update.effective_user.id
    user = update.effective_user
    user_info = f"{user.full_name} (@{user.username}) [{user.id}]"
    user_message = update.message.text

    log_message(user_info, "USER", user_message)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    if user_id not in user_data:
        user_data[user_id] = {"history": [], "model": DEFAULT_MODEL}

    model = user_data[user_id]["model"]
    history = user_data[user_id]["history"]
    history.append({"role": "user", "content": user_message})

    try:
        response = ollama.chat(model=model, messages=history, options={"num_predict": 1024, "timeout": 120})
        reply = response["message"]["content"]
        log_message(user_info, "BOT", reply[:100] + "..." if len(reply) > 100 else reply)
    except Exception as e:
        reply = f"❌ Ошибка Ollama: {e}"
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

        model = user_data[user_id]["model"]
        history = user_data[user_id]["history"]
        if history and history[-1]["role"] == "assistant":
            history.pop()

        try:
            response = ollama.chat(model=model, messages=history, options={"num_predict": 1024, "timeout": 120})
            new_reply = response["message"]["content"]
        except Exception as e:
            new_reply = f"❌ Ошибка: {e}"
        else:
            history.append({"role": "assistant", "content": new_reply})
            last_interaction[user_id]["reply"] = new_reply

        await query.edit_message_text(new_reply, reply_markup=get_buttons())

def main():
    print(f"🤖 Бот запущен с кнопками оценки. Логи: {LOG_FILE}")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("model", set_model))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()