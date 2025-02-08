# AbzumsAI Q&A Bot

This is a Telegram bot for answering questions about AbzumsAI Educational Institute. The bot provides a list of predefined questions and their answers. Users can get answers by sending the question number, the full question text, or part of the question. It also lets users submit feature suggestions and institute improvement ideas.

## Features

- **Start:** Sends a welcome message with instructions.
- **Help:** Shows a list of all available commands and how to use them.
- **Questions:** Displays a list of predefined questions.
- **Random:** Returns a random question and answer.
- **Search:** Lets you search for questions by a keyword. (Usage example: `search math`)
- **Newfeature:** For sending a new feature suggestion. The original message is forwarded to the bot admin.
- **Newsuggestion:** For sending improvement suggestions for the institute. This message is forwarded to the institute's chat.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AbzumsAI/QA-Bot.git
   cd QA-Bot
   ```

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file in the project root with the following variables:**
   ```
   TELEGRAM_API_TOKEN=telegram_api_token_here
   ADMIN_CHAT_ID=admin_chat_id_here
   INSTITUTE_CHAT_ID=institute_chat_id_here
   ```
   To find your chat ID, you can use bots like [@userinfobot](https://t.me/userinfobot) or check the output of getUpdates.

4. **Run the bot:**
   ```bash
   python bot.py
   ```

## How to Use

- **start** - Displays the welcome message and instructions.
- **help** - Shows all available commands and explains how to ask questions.
- **questions** - Lists all predefined questions. You can answer by sending the question number or text.
- **random** - Sends a random question and its answer.
- **search** - Searches questions by a given keyword (e.g., `search math`).
- **newfeature** - Sends your feature suggestion to the bot admin (your suggestion is forwarded with your chat info).
- **newsuggestion** - Sends your improvement suggestion for the institute to the institute's chat.

Enjoy using the bot and feel free to contribute with suggestions!