import telebot
import discord
from discord.ext import commands
import asyncio
import threading
from flask import Flask
import os

# Використовуємо змінні оточення для токенів та інших конфіденційних даних
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
discord_bot_token = os.getenv('DISCORD_BOT_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

# Імпортуємо Intents для Discord
intents = discord.Intents.default()
intents.message_content = True  # Дозволяємо боту читати контент повідомлень

# Створюємо бота з параметром intents
discord_bot = commands.Bot(command_prefix='!', intents=intents)

# Telegram Bot
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

# Функція для запуску Telegram бота у фоновому потоці
def run_telegram_bot():
    telegram_bot.polling(none_stop=True)

# Функція для запуску Discord бота
async def run_discord_bot():
    await discord_bot.start(discord_bot_token)

# Flask маршрут для перевірки статусу сервера
@app.route('/')
def home():
    return "Бот працює!"

# Основна функція для запуску обох ботів
if __name__ == "__main__":
    # Запускаємо Telegram бота в окремому потоці
    telegram_thread = threading.Thread(target=run_telegram_bot)
    telegram_thread.start()

    # Запускаємо Flask для прослуховування порту
    port = int(os.environ.get('PORT', 5000))  # Render надасть порт через змінну PORT
    app.run(host='0.0.0.0', port=port)

    # Запускаємо Discord бота в основному потоці (асинхронно)
    asyncio.run(run_discord_bot())
