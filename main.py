import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
PUBLIC_URL = os.environ["PUBLIC_URL"]  # ex: https://ton-service.onrender.com

# --- Telegram bot setup ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot webhook actif !")

application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

# --- Flask web server (for Render Web Service) ---
app = Flask(__name__)

@app.get("/")
def health():
    return "ok", 200

@app.post("/webhook")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(application.process_update(update))
    loop.close()

    return "ok", 200


if __name__ == "__main__":
    # Local run only; Render will use gunicorn
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "10000")))
