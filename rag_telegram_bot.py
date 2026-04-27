import os
import asyncio
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gigachat import GigaChat
import fitz  # PyMuPDF

# --- НАСТРОЙКИ ---
TOKEN = os.environ.get("TOKEN", "8635674583:AAGstQqoxW4u6vl_XSJLgbkB2zsgY953O_0")
GIGACHAT_KEY = os.environ.get("GIGACHAT_KEY", "MDE5ZGExZDctMzU3Ni03ODBhLWI5NTItOTc0NjlmY2E5YmNmOjZlMDQ3M2JlLTg4Y2QtNDQ2Ny1hNjk2LTE1NTU2ODZjMjQ0Zg==")

# Хранилище текста загруженных PDF (в памяти)
pdf_text_storage = {}

# --- Команды бота ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    await update.message.reply_text(
        "📚 Привет! Я RAG-бот без LangChain.\n"
        "1. Отправь мне PDF-файл, и я его запомню.\n"
        "2. Потом задай вопрос командой: /ask <твой вопрос>\n"
        "3. Посмотри, сколько файлов загружено: /list"
    )

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка загруженных PDF-файлов."""
    document = update.message.document
    if not document or not document.file_name.lower().endswith('.pdf'):
        return

    await update.message.reply_text("⏳ Обрабатываю PDF...")
    user_id = update.effective_user.id
    file = await context.bot.get_file(document.file_id)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        await file.download_to_drive(tmp.name)
        doc = fitz.open(tmp.name)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()

    if not full_text.strip():
        await update.message.reply_text("❌ Не удалось извлечь текст из PDF. Возможно, это изображение.")
        return

    # Сохраняем текст в памяти (для каждого пользователя свой)
    if user_id not in pdf_text_storage:
        pdf_text_storage[user_id] = []
    pdf_text_storage[user_id].append({
        "file_name": document.file_name,
        "text": full_text
    })

    await update.message.reply_text(f"✅ PDF обработан! Всего файлов у вас: {len(pdf_text_storage[user_id])}")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ответ на вопрос по загруженным документам."""
    if update.message is None:
        return
    user_id = update.effective_user.id
    question = ' '.join(context.args) if context.args else None

    if not question:
        await update.message.reply_text("❌ Напиши вопрос после /ask. Например: /ask Что такое MLOps?")
        return

    if user_id not in pdf_text_storage or not pdf_text_storage[user_id]:
        await update.message.reply_text("❌ У вас нет загруженных документов. Сначала отправьте PDF-файл.")
        return

    await update.message.reply_text("🔍 Ищу ответ в документах...")

    # Берём текст из последнего загруженного PDF
    all_texts = [item['text'] for item in pdf_text_storage[user_id]]
    combined_text = "\n\n".join(all_texts)

    # Если текст слишком большой, берём первые 3000 символов
    if len(combined_text) > 3000:
        combined_text = combined_text[:3000] + "..."

    # Отправляем в GigaChat
    try:
        client = GigaChat(credentials=GIGACHAT_KEY, verify_ssl_certs=False)
        prompt = f"Ответь на вопрос, используя ТОЛЬКО следующий контекст из PDF-файла. Если ответа нет в контексте, скажи об этом.\n\nКонтекст:\n{combined_text}\n\nВопрос: {question}\nОтвет:"
        response = client.chat({"messages": [{"role": "user", "content": prompt}]})
        answer = response.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при поиске ответа: {e}")

async def list_docs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать список загруженных файлов."""
    user_id = update.effective_user.id
    if user_id not in pdf_text_storage or not pdf_text_storage[user_id]:
        await update.message.reply_text("📂 У вас нет загруженных документов.")
        return

    file_names = [item['file_name'] for item in pdf_text_storage[user_id]]
    await update.message.reply_text(f"📂 Загруженные файлы:\n" + "\n".join(f"- {name}" for name in file_names))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("list", list_docs))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    print("📚 RAG-бот (без LangChain) запущен. Отправьте PDF-файл и спрашивайте!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()