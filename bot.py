import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "9152510017:AAEIewVXdoQs77-DhdCsYAp3XPypZKCEbiQ"

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = "downloaded_quiz.txt"
    try:
        document = update.message.document
        if not document.file_name.endswith('.txt'):
            await update.message.reply_text("দয়া করে শুধুমাত্র .txt ফরম্যাটের ফাইল আপলোড করুন!")
            return
        file = await context.bot.get_file(document.file_id)
        await file.download_to_drive(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        await update.message.reply_text("ফাইল সফলভাবে পাওয়া গেছে! কুইজ তৈরি হচ্ছে... 🚀")
        raw_questions = content.split("Q:")
        success_count = 0
        for item in raw_questions:
            if not item.strip():
                continue
            lines = [line.strip() for line in item.strip().split("\n") if line.strip()]
            if len(lines) < 6:
                continue 
            question_text = lines[0]
            options = [lines[1][2:].strip(), lines[2][2:].strip(), lines[3][2:].strip(), lines[4][2:].strip()]
            correct_line = lines[5]
            correct_char = correct_line.split(":")[-1].strip().upper()
            correct_index = ord(correct_char) - ord('A')
            await context.bot.send_poll(
                chat_id=update.effective_chat.id,
                question=question_text,
                options=options,
                type='quiz',
                correct_option_id=correct_index
            )
            success_count += 1
        await update.message.reply_text(f"মোট {success_count} টি কুইজ সফলভাবে পাঠানো হয়েছে! 🎉")
    except Exception as e:
        await update.message.reply_text(f"একটি ত্রুটি ঘটেছে: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.Document.TXT, handle_document))
    print("বট সফলভাবে রান হচ্ছে... টেলিগ্রামে ফাইল পাঠান।")
    app.run_polling()

if __name__ == '__main__':
    main()
          
