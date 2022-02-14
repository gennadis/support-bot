# Telegram, Vk Support Bot

This project automates answering popular questions in your Vk group or in Telegram.
With [Google DialogFlow](https://cloud.google.com/dialogflow/docs/) you can handle these questions with ease - just train your own neural network model with question-answer templates.

![Screenshot](Screenshot.png)

## Features
- `long polling` VK and Telegram API utilization
- Answer user's questions with pre-trained `DialogFlow` model
- Train your `DialogFlow` from local JSON file
- Heroku ready!

## Installation
1. Clone project
```bash
git clone https://github.com/gennadis/support-bot
cd support-bot
```

2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install requirements
```bash
pip install -r requirements.txt
```

4. Rename `.env.example` to `.env` and fill your secrets in it.  

5. Run bots
```bash
python tg_bot.py
python vk_bot.py
```

## Examples
To create and upload your intents automatically:
1. Create a JSON file according to the `dvmn_questions.json` example
2. Run 
```bash
python flow.py --add your_intents_filename.json
```
