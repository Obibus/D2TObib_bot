import os
import telebot
import discord
from discord.ext import commands
from flask import Flask, request
import threading

# Використовуємо змінні оточення для токенів та інших конфіденційних даних
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
discord_bot_token = os.getenv('DISCORD_BOT_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
webhook_url = os.getenv('WEBHOOK_URL')

# Імпортуємо Intents для Discord
intents = discord.Intents.default()
intents.message_content = True

# Створюємо Discord бота
discord_bot = commands.Bot(command_prefix='!', intents=intents)

# Створюємо Telegram бота
telegram_bot = telebot.TeleBot(telegram_bot_token)

# Flask для відкриття порту
app = Flask(__name__)

# Telegram бот: команда /start
@telegram_bot.message_handler(commands=['start'])
def send_welcome(message):
    telegram_bot.send_message(message.chat.id, 'Привіт!')

# Discord бот: готовність
@discord_bot.event
async def on_ready():
    print(f'Discord бот запущено як {discord_bot.user}')

# Команда в Discord для відправки повідомлення в Telegram
@discord_bot.command()
async def send_to_telegram(ctx, *, message):
    telegram_bot.send_message(telegram_chat_id, message)
    await ctx.send('Повідомлення надіслано в Telegram!')

# Flask маршрут для вебхука
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    telegram_bot.process_new_updates([update])
    return '!', 200

# Flask маршрут для перевірки статусу сервера
@app.route('/')
def home():
    return "Бот працює!"

# Функція для запуску Flask серверу
def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# Функція для запуску Discord бота
def run_discord():
    discord_bot.run(discord_bot_token)

if __name__ == "__main__":
    # Запускаємо Flask сервер в окремому потоці
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Запускаємо Discord бота в головному потоці
    run_discord()
