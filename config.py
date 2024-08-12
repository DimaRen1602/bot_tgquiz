import logging
from aiogram import Bot, Dispatcher

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Токен бота
API_TOKEN = 'YOUR_TGBOTAPI_KEY'

# Объект бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Имя базы данных
DB_NAME = 'quiz_bot.db'
