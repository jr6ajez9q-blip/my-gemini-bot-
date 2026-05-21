import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# Logging စနစ် ပြင်ဆင်ခြင်း
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Render ၏ Environment Variables မှ Key များကို ဆွဲယူခြင်း (လုံခြုံရေးအတွက်)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini Client စတင်ခြင်း
client = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။ ကျွန်တော်က Gemini AI Bot ဖြစ်ပါတယ်။ ဘာကူညီပေးရမလဲခင်ဗျာ။")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # စာပြန်နေစဉ် ဖုန်းမှာ typing... ပြနေစေရန်
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Gemini-2.5-flash ကို သုံးပြီး အဖြေတောင်းခြင်း
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("စိတ်မရှိပါနဲ့ဗျာ၊ တစ်ခုခုမှားယွင်းသွားလို့ ခဏနေမှ ပြန်စမ်းကြည့်ပေးပါ။")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()