import asyncio
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
import nest_asyncio

# Load environment variables from .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROUP_CHAT_ID = -4909485308  # Replace with your real group chat ID

# Command: /sales
async def sales_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text='លក់បានទេអ្នកទាំងអស់គ្នា')

# Auto scheduled message
async def scheduled_daily_message(app):
    await app.bot.send_message(chat_id=GROUP_CHAT_ID, text='លក់បានទេអ្នកទាំងអស់គ្នា')

# Main bot setup
async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Only allow /sales command
    app.add_handler(CommandHandler('sales', sales_command))

    # Scheduler for auto message
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        scheduled_daily_message,
        'cron',
        hour=23,
        minute=3,
        args=(app,),
        timezone=pytz.timezone('Asia/Phnom_Penh')
    )
    scheduler.start()

    print("✅ Bot is running... ")
    await app.run_polling()

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())
