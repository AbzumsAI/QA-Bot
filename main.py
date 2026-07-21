import os
import time
import requests
import random
from dotenv import load_dotenv
from qa import qa

load_dotenv()

TOKEN = os.getenv("TELEGRAM_API_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
INSTITUTE_CHAT_ID = os.getenv("INSTITUTE_CHAT_ID")
REQUEST_TIMEOUT = int(os.getenv("TELEGRAM_REQUEST_TIMEOUT", "10"))
POLL_TIMEOUT = int(os.getenv("TELEGRAM_POLL_TIMEOUT", "20"))


def get_base_url():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_API_TOKEN is not set")
    return f"https://api.telegram.org/bot{TOKEN}"


def telegram_request(method, params=None, timeout=REQUEST_TIMEOUT):
    url = f"{get_base_url()}/{method}"
    response = requests.get(url, params=params or {}, timeout=timeout)
    response.raise_for_status()
    return response.json()


def split_command(text):
    if not text.startswith("/"):
        return None, text
    command, _, argument = text.partition(" ")
    return command.split("@", 1)[0].lower(), argument.strip()


def normalize_lookup_text(text):
    return " ".join(text.strip().lower().split())


def find_matching_questions(text, questions):
    keyword = normalize_lookup_text(text)
    if not keyword:
        return []
    return [question for question in questions if keyword in question.lower()]


def build_numbered_lines(items):
    return "".join(f"{index}. {item}\n" for index, item in enumerate(items, 1))


def select_question_by_number(text, questions):
    if not text.isdigit():
        return None
    index = int(text) - 1
    if 0 <= index < len(questions):
        return questions[index]
    return None


def get_updates(offset=None):
    params = {"timeout": POLL_TIMEOUT}
    if offset is not None:
        params["offset"] = offset
    try:
        return telegram_request(
            "getUpdates",
            params=params,
            timeout=POLL_TIMEOUT + REQUEST_TIMEOUT,
        )
    except requests.RequestException as error:
        return {"ok": False, "description": str(error)}


def send_message(chat_id, text, reply_markup=None):
    params = {"chat_id": chat_id, "text": text}
    if reply_markup:
        params["reply_markup"] = reply_markup
    return telegram_request("sendMessage", params=params)


def forward_message(to_chat_id, from_chat_id, message_id):
    params = {
        "chat_id": to_chat_id,
        "from_chat_id": from_chat_id,
        "message_id": message_id
    }
    return telegram_request("forwardMessage", params=params)


def main():
    offset = None
    while True:
        updates = get_updates(offset)
        if updates.get("ok"):
            for update in updates["result"]:
                offset = update["update_id"] + 1
                message = update.get("message")
                if not message:
                    continue
                chat_id = message["chat"]["id"]
                text = message.get("text", "").strip()
                command, argument = split_command(text)
                if command == "/start":

                    start_text = (
                        "سلام!\n\n"
                        "به بات پرسش و پاسخ اولین برنامه جامع آموزشی مقدمات هوش مصنوعی خوش آمدید.\n\n"
                        "این بات به شما امکان می‌دهد تا به سادگی از میان سوالات از پیش تعریف‌شده، "
                        "یا با ارسال شماره، متن کامل یا بخشی از سوال، پاسخ مورد نظر خود را دریافت کنید.\n\n"
                        "برای مشاهده راهنما و دستورات موجود، دستور /help را ارسال کنید.\n"
                        "همچنین در صورت تمایل به ارسال پیشنهاد برای فیچرهای جدید، از دستور /newfeature استفاده نمایید. "
                        "پیشنهاد شما برای سازنده بات ارسال خواهد شد.\n\n"
                        "اگر پیشنهادی برای بهبود برنامه‌ی جامع آموزشی مقدمات هوش مصنوعی دارید، می‌توانید از دستور /newsuggestion استفاده کنید.\n\n"
                    )

                    send_message(chat_id, start_text)

                    continue
                if command == "/help":
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
                        "/search\n"
                        "جستجو در سوالات بر اساس کلمه کلیدی (مثال: search ریاضی).\n\n"
                        "/newfeature\n"
                        "ارسال پیشنهاد فیچر جدید به سازنده بات به صورت فوروارد (مثال: /newfeature پیشنهاد بهبود).\n\n"
                        "/newsuggestion\n"
                        "ارسال پیشنهاد بهبود برای برنامه جامع آموزشی مقدمات هوش مصنوعی به صورت فوروارد (مثال: /newsuggestion پیشنهاد بهبود).\n\n"
                        "برای دریافت پاسخ از سوالات، شما می‌توانید:\n"
                        "1. شماره سوال را ارسال کنید (مثلاً 1 برای سوال اول)،\n"
                        "2. متن کامل سوال را وارد کنید، یا\n"
                        "3. بخشی از سوال را ارسال کنید تا در میان سوالات جستجو شود.\n"
                    )
                    send_message(chat_id, help_text)
                    continue
                if command == "/questions":
                    qlist = "لیست سوالات (برای دریافت پاسخ، شماره یا متن سوال را ارسال کنید):\n\n"
                    questions = list(qa.keys())
                    qlist += build_numbered_lines(questions)
                    send_message(chat_id, qlist)
                    continue
                if command == "/random":
                    questions = list(qa.keys())
                    random_question = random.choice(questions)
                    answer = qa[random_question]
                    send_message(
                        chat_id, f"سوال: {random_question}\n\nپاسخ: {answer}")
                    continue
                if command == "/search":
                    if not argument:
                        send_message(
                            chat_id, "برای استفاده از دستور /search، باید پس از کلمه /search، کلمه کلیدی را وارد کنید.\nمثال: /search ریاضی")
                        continue
                    matching = find_matching_questions(argument, qa.keys())
                    if matching:
                        result = "سوالات پیدا شده:\n\n"
                        result += build_numbered_lines(matching)
                        send_message(chat_id, result)
                    else:
                        send_message(
                            chat_id, "سوالی با این کلمه کلیدی یافت نشد.")
                    continue
                if command == "/newfeature":
                    if not argument:
                        send_message(
                            chat_id, "برای ارسال پیشنهاد فیچر جدید، دستور را به صورت:\n/newfeature متن پیشنهاد\nارسال کنید.")
                        continue
                    forward_message(ADMIN_CHAT_ID, chat_id,
                                    message["message_id"])
                    send_message(
                        chat_id, "پیشنهاد شما برای بهبود بات با موفقیت ارسال شد. سپاسگزاریم.")
                    continue
                if command == "/newsuggestion":
                    if not argument:
                        send_message(
                            chat_id, "برای ارسال پیشنهاد بهبود برای موسسه، دستور را به صورت:\n/newsuggestion متن پیشنهاد\nارسال کنید.")
                        continue
                    forward_message(INSTITUTE_CHAT_ID, chat_id,
                                    message["message_id"])
                    send_message(
                        chat_id, "پیشنهاد شما برای بهبود برنامه جامع آموزشی مقدمات هوش مصنوعی با موفقیت ارسال شد. سپاسگزاریم.")
                    continue
                if text.isdigit():
                    questions = list(qa.keys())
                    selected_question = select_question_by_number(text, questions)
                    if selected_question:
                        send_message(
                            chat_id, f"سوال: {selected_question}\n\nپاسخ: {qa[selected_question]}")
                        continue
                matching = find_matching_questions(text, qa.keys())
                if matching:
                    if len(matching) == 1:
                        selected_question = matching[0]
                        send_message(
                            chat_id, f"سوال: {selected_question}\n\nپاسخ: {qa[selected_question]}")
                    else:
                        result = "سوالات مشابه پیدا شده:\n\n"
                        result += build_numbered_lines(matching)
                        send_message(chat_id, result)
                else:
                    send_message(chat_id, "جوابی برای این سوال موجود نیست.")
        time.sleep(1)


if __name__ == "__main__":
    main()
