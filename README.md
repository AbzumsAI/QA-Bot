# AbzumsAI Q&A Bot

I keep this repo for the Telegram bot that answers common questions about the AbzumsAI Educational Institute. The bot works from a fixed question list, so people can ask by number, full text, or a small part of a question.

It also forwards two kinds of messages:

- New bot feature ideas go to the bot admin.
- Institute suggestions go to the institute chat.

## Run It Locally

Clone the repo and install the packages:

```bash
git clone https://github.com/AbzumsAI/QA-Bot.git
cd QA-Bot
pip install -r requirements.txt
```

Create a `.env` file:

```env
TELEGRAM_API_TOKEN=telegram_api_token_here
ADMIN_CHAT_ID=admin_chat_id_here
INSTITUTE_CHAT_ID=institute_chat_id_here
```

Optional settings:

- `TELEGRAM_REQUEST_TIMEOUT` sets the normal request timeout in seconds. The default is `10`.
- `TELEGRAM_POLL_TIMEOUT` sets the Telegram long poll timeout in seconds. The default is `20`.

Run the bot:

```bash
python main.py
```

## Bot Commands

- `/start` shows the welcome text.
- `/help` shows the command guide.
- `/questions` lists all saved questions.
- `/random` sends one random question with its answer.
- `/search math` searches the questions for a word.
- `/newfeature my idea` forwards a bot idea to the admin.
- `/newsuggestion my idea` forwards an institute idea to the institute chat.

The bot also accepts command mentions such as `/help@YourBotName`, which Telegram may send in group chats.

## Checks I Run

The tests cover command parsing and text matching. Run them before changing the bot flow:

```bash
python -m unittest discover -s tests
```
