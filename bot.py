import asyncio
import openai
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, ContextTypes, MessageHandler,
    CommandHandler, filters
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Load environment variables from .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GROUP_CHAT_ID = -4898266114  # Replace with your real chat ID

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY


# Handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}],
            max_tokens=150,
            temperature=0.7,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Sorry, something went wrong: {e}"
    await update.message.reply_text(reply)


# /sales command handler
async def sales_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('លក់បានទេអ្នកទាំងអស់គ្នា')


# Auto scheduled message
async def scheduled_daily_message(app):
    await app.bot.send_message(chat_id=GROUP_CHAT_ID, text='លក់បានទេអ្នកទាំងអស់គ្នា')


# Main bot setup
async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler('sales', sales_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        scheduled_daily_message,
        'cron',
        hour=22,  # 10PM
        minute=22,
        args=(app,)
    )
    scheduler.start()

    print("Your GPT bot is running...")
    await app.run_polling()


if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
