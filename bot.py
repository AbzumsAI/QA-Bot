import os
import time
import requests
import random
from dotenv import load_dotenv
from qa import qa
from config import  ADMIN_CHAT_ID , INSTITUTE_CHAT_ID , BASE_URL



def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"
    params = {}
    if offset:
        params["offset"] = offset
    r = requests.get(url, params=params)
    return r.json()

def send_message(chat_id, text, reply_markup=None):
    url = f"{BASE_URL}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    if reply_markup:
        params["reply_markup"] = reply_markup
    response = requests.get(url, params=params)
    return response.json()

def main():
    offset = None
    awaiting_response = {}  # Track users who are submitting suggestions (new feature or suggestion)

    while True:
        updates = get_updates(offset)
        if updates.get("ok"):
            for update in updates["result"]:
                offset = update["update_id"] + 1  # Increment offset to avoid reprocessing same updates
                message = update.get("message")
                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text", "").strip()
                first_name = message["from"].get("first_name", "دوست عزیز")

                # Welcome message
                if text == "/start":
                    start_text = (
                        f"سلام {first_name}!\n\n"
                        "به بات پرسش و پاسخ اولین برنامه جامع آموزشی مقدمات هوش مصنوعی خوش آمدید.\n\n"
                        "این بات به شما امکان می‌دهد تا به سادگی از میان سوالات از پیش تعریف‌شده، "
                        "یا با ارسال شماره، متن کامل یا بخشی از سوال، پاسخ مورد نظر خود را دریافت کنید.\n\n"
                        "برای مشاهده راهنما و دستورات موجود، دستور /help را ارسال کنید.\n"
                        "همچنین در صورت تمایل به ارسال پیشنهاد برای فیچرهای جدید، از دستور /newfeature استفاده نمایید.\n\n"
                    )
                    send_message(chat_id, start_text)
                    continue

                # Help message to guide users through commands
                if text == "/help":
                    help_text = (
                        "دستورات موجود:\n\n"
                        "/start\n"
                        "نمایش پیام خوش‌آمدگویی و توضیحات کامل درباره بات و نحوه استفاده.\n\n"
                        "/help\n"
                        "نمایش راهنمای دستورات و توضیحات نحوه پرسیدن سوال.\n\n"
                        "/questions\n"
                        "نمایش لیست سوالات از پیش تعریف‌شده به همراه دستورالعمل استفاده.\n\n"
                        "/random\n"
                        "دریافت یک پرسش و پاسخ تصادفی با فاصله مناسب بین سوال و پاسخ.\n\n"
                        "/search [کلمه کلیدی]\n"
                        "جستجو در سوالات بر اساس کلمه کلیدی (مثال: search ریاضی).\n\n"
                        "/newfeature\n"
                        "ارسال پیشنهاد فیچر جدید به سازنده بات.\n\n"
                        "/newsuggestion\n"
                        "ارسال پیشنهاد بهبود برای موسسه.\n\n"
                        "برای دریافت پاسخ از سوالات، شما می‌توانید:\n"
                        "1. شماره سوال را ارسال کنید (مثلاً 1 برای سوال اول)،\n"
                        "2. متن کامل سوال را وارد کنید، یا\n"
                        "3. بخشی از سوال را ارسال کنید تا در میان سوالات جستجو شود.\n"
                    )
                    send_message(chat_id, help_text)
                    continue

                # Listing all predefined questions
                if text == "/questions":
                    qlist = "لیست سوالات (برای دریافت پاسخ، شماره یا متن سوال را ارسال کنید):\n\n"
                    questions = list(qa.keys())
                    for i, q in enumerate(questions, 1):
                        qlist += f"{i}. {q}\n"
                    send_message(chat_id, qlist)
                    continue

                # Sending a random question and answer
                if text == "/random":
                    questions = list(qa.keys())
                    random_question = random.choice(questions)
                    answer = qa[random_question]
                    send_message(chat_id, f"سوال: {random_question}\n\nپاسخ: {answer}")
                    continue

                # Searching for a keyword in predefined questions
                if text.startswith("/search"):
                    parts = text.split(maxsplit=1)
                    if len(parts) < 2 or not parts[1].strip():
                        send_message(chat_id, "برای استفاده از دستور search، باید پس از کلمه search، کلمه کلیدی را وارد کنید.\nمثال: search ریاضی")
                        continue
                    keyword = parts[1].strip().lower()

                    # Searching questions based on the keyword
                    matching = [q for q in qa.keys() if keyword in q.lower()]
                    if matching:
                        result = "سوالات پیدا شده:\n\n"
                        for i, q in enumerate(matching, 1):
                            # Getting the actual question index from the original list
                            real_idx = list(qa.keys()).index(q) + 1
                            result += f"{real_idx}. {q}\n"
                        send_message(chat_id, result)
                    else:
                        send_message(chat_id, "سوالی با این کلمه کلیدی یافت نشد.")
                    continue

                # Requesting new feature suggestions from users (this will send for admin account)
                if text == "/newfeature":
                    send_message(chat_id, "لطفاً پیشنهاد فیچر جدید خود را ارسال کنید. پیام شما برای سازنده بات ارسال خواهد شد.")
                    awaiting_response[chat_id] = "newfeature"  # Track that the user is submitting a new feature suggestion
                    continue

                # Requesting suggestions for improvements for the institute (this will send for institute account )
                if text == "/newsuggestion":
                    send_message(chat_id, "لطفاً پیشنهاد بهبود خود را ارسال کنید. پیام شما برای موسسه ارسال خواهد شد.")
                    awaiting_response[chat_id] = "newsuggestion"  # Track that the user is submitting an improvement suggestion
                    continue

                # Handling received suggestions and forwarding to admin/institute
                if chat_id in awaiting_response:
                    if awaiting_response[chat_id] == "newfeature":
                        feature_message = f"پیشنهاد فیچر جدید از {first_name}:\n{text}"
                        send_message(chat_id, "پیشنهاد شما برای فیچر جدید ثبت و ارسال شد. سپاسگزاریم.")
                        send_message(ADMIN_CHAT_ID, feature_message)  # Forwarding feature suggestion to admin
                    elif awaiting_response[chat_id] == "newsuggestion":
                        suggestion_message = f"پیشنهاد بهبود از {first_name}:\n{text}"
                        send_message(chat_id, "پیشنهاد شما برای بهبود برنامه ثبت و ارسال شد. سپاسگزاریم.")
                        send_message(INSTITUTE_CHAT_ID, suggestion_message)  # Forwarding suggestion to institute
                    del awaiting_response[chat_id]  # Clearing the user state after submission
                    continue

                # Handling responses when user inputs a number (selecting specific question)
                if text.isdigit():
                    idx = int(text) - 1
                    questions = list(qa.keys())
                    if 0 <= idx < len(questions):
                        selected_question = questions[idx]
                        send_message(chat_id, f"سوال: {selected_question}\n\nپاسخ: {qa[selected_question]}")
                    else:
                        send_message(chat_id, "شماره سوال وارد شده معتبر نیست.")
                    continue

                # Searching for matching questions based on user input
                matching = [q for q in qa.keys() if text.lower() in q.lower()]
                if matching:
                    if len(matching) == 1:
                        selected_question = matching[0]
                        send_message(chat_id, f"سوال: {selected_question}\n\nپاسخ: {qa[selected_question]}") 
                    else:
                        result = "سوالات مشابه پیدا شده:\n\n"
                        for i, q in enumerate(matching, 1):
                            # Getting the actual question index from the original list
                            real_idx = list(qa.keys()).index(q) + 1
                            result += f"{real_idx}. {q}\n"
                        send_message(chat_id, result)
                else:
                    send_message(chat_id, "لطفاً از دکمه /help برای مشاهده دستورات استفاده کنید.")
        time.sleep(1)

if __name__ == "__main__":
    main()
