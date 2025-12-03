import asyncio
import time

import telebot.async_telebot as telebot
from deepseekcode1 import *
from allprompt import *
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("BOT_TOKEN")
bot = telebot.AsyncTeleBot(token)
admin_id = os.getenv("ADMIN_ID")

async def premes(message):
    sent_message = await bot.send_message(message.chat.id, '🕒Нейрожириновский думает над ответом...🕒')
    return sent_message.message_id


@bot.message_handler(commands=['ask'])
async def ren(message):
    try:
        nc = message.text.replace("/ask", "").strip().replace('@aizhirinovskiy_bot', '').strip()

        if nc:
            # Отправляем сообщение о загрузке
            loading_msg_id = await premes(message)

            # Получаем ответ от нейросети
            res = await routerai(nc, get_prompt(message.chat.id))

            # Удаляем сообщение о загрузке и отправляем результат
            await bot.delete_message(message.chat.id, loading_msg_id)
            await bot.reply_to(message, res)
        else:
            await bot.reply_to(message, "Напишите сообщение после команды /ask")
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(content_types=['photo'])
async def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = await bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{token}/{file_info.file_path}"
        loading_msg_id = await premes(message)
        res= await photoai(file_url, get_prompt(message.chat.id))
        await bot.delete_message(message.chat.id, loading_msg_id)
        await bot.reply_to(message, res)
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['prompt'])
async def ren(message):
    try:

        nc = message.text.replace("/prompt", "").strip().replace('@aizhirinovskiy_bot', '').strip()
        if nc:
            change_prompt(message.chat.id, nc)
            await bot.send_message(message.chat.id, "Промпт для вашего чата успешно изменён")
        else:
            await bot.send_message(message.chat.id, "Напишите промпт после команды /prompt")
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['default'])
async def ren(message):
    try:
        reset_prompt(message.chat.id)
        await bot.send_message(message.chat.id, "Промпт для вашего чата успешно сброшен")
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['check'])
async def ren(message):
    try:
        prompt = get_prompt(message.chat.id)
        if prompt:
            await bot.send_message(message.chat.id, f"Промпт текущего чата: {prompt}")
        elif not prompt:
            await bot.send_message(message.chat.id, f"Промпт текущего чата отсутствует, чтобы добавить промпт пропишите /prompt")
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['start'])
async def ren(message):
    try:
        await bot.send_message(message.chat.id, 'я, Нейрожириновский, расскажу тебе свое мнение о чем либо. \
Очень сильно матерюсь и предвзято отношусь к людям. Спроси меня о чем-то через /ask или просто отправь фото\n\n\
Разработчик текущей версии: <i>@endurra</i>\n\nПроцесс разработки и полезная информация: <i>@codebykrais</i>', parse_mode='HTML')
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['log'])
async def ren(message):
    try:
        if message.from_user.id == admin_id:
            await bot.send_message(message.chat.id, f'''Лог от [{current_time()}]:
            
Текущий api-ключ: {index_api_key}

База данных:
{get_db()}''')
        else: await bot.send_message(message.chat.id, 'Вы не владеете правами админитсратора!')
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")

async def main():
    while True:
        try:
            print("Бот запущен в асинхронном режиме!")
            await bot.delete_webhook(drop_pending_updates=True)
            print("Вебхуки удалены")
            await bot.infinity_polling(skip_pending=True, timeout=300)
        except Exception as e:
            print(f'[{current_time()}] Ошибка: {e}')
            time.sleep(15)


if __name__ == "__main__":
    asyncio.run(main())