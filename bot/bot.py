# Импорт стандартных библиотек
import os               # Для работы с переменными окружения (токены)
import logging          # Для логирования событий (отладка и ошибки)

# Импорт классов Telegram API
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,    # Строит Telegram-приложение
    CommandHandler,        # Обработчик команд типа /start
    MessageHandler,        # Обработчик обычных сообщений
    ContextTypes,          # Контекст, передаваемый в колбэки
    filters                # Фильтры сообщений (например, только текст)
)

# Импорт OpenAI SDK
import openai

# Настройка логов — полезно для отладки (можно выводить ошибки в консоль)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем токены из переменных окружения (лучше, чем хардкодить в коде)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Устанавливаем ключ для OpenAI
openai.api_key = OPENAI_API_KEY


# ----------------------------- Команда /start -----------------------------

# Функция вызывается, когда пользователь вводит команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот с ИИ. Напиши мне что-нибудь.")


# --------------------------- Ответ на сообщение --------------------------

# Эта функция вызывается, когда пользователь отправляет обычное текстовое сообщение
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text  # Сохраняем сообщение пользователя

    # Отправляем сообщение в OpenAI (GPT-3.5)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Используемый LLM
        messages=[
            {"role": "system", "content": "Ты дружелюбный помощник."},  # Начальные инструкции модели
            {"role": "user", "content": user_message}  # Само сообщение пользователя
        ]
    )

    # Получаем сгенерированный ответ
    bot_reply = response['choices'][0]['message']['content']

    # Отправляем его обратно пользователю
    await update.message.reply_text(bot_reply)


# ------------------------- Точка входа в программу ------------------------

def main():
    # Создаём экземпляр Telegram-приложения и передаём токен
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Добавляем обработчик команды /start
    app.add_handler(CommandHandler("start", start))

    # Добавляем обработчик всех текстовых сообщений (кроме команд)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Выводим сообщение в консоль, что бот запущен
    print("Бот запущен...")

    # Запускаем бесконечный цикл обработки входящих сообщений
    app.run_polling()


# Запускаем main() если запускается напрямую
if __name__ == '__main__':
    main()
