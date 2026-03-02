import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from db import init_db, save_contact

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not BOT_TOKEN or not CHANNEL_ID:
    raise ValueError("Помилка: задайте BOT_TOKEN і CHANNEL_ID у файлі .env")

init_db()

waiting_for_contact = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    waiting_for_contact.add(chat_id)
    await update.message.reply_text("Привіт! Надішліть свою контактну інформацію 👇")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text

    if chat_id in waiting_for_contact:
        waiting_for_contact.remove(chat_id)
        save_contact(chat_id, text)
        await update.message.reply_text("Супер! Записав.")

        # Надсилаємо контакт у канал
        try:
            await context.bot.send_message(chat_id=int(CHANNEL_ID), text=f"Новий контакт від {chat_id}:\n{text}")
        except Exception as e:
            print(f"Помилка надсилання у канал: {e}")

    else:
        await update.message.reply_text("Надішліть /start, щоб почати.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущений. Надішліть /start у Telegram.")
    app.run_polling()

if __name__ == "__main__":
    main()
