import asyncio
import json
import os
import re
import aioschedule
import redis
import requests
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.types import ParseMode
from aiogram.types import WebAppInfo
from aiogram.utils import executor
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      BotKicked)
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv('TOKEN_BOT'))
dp = Dispatcher(bot)
redis_host = 'redis'
redis_port = 6379
redis_db = 0
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

async def check_and_send_notifications():
    while True:
        # Пытаемся получить задачу из Redis (блокирующий вызов с таймаутом в 1 секунду)
        task_data = redis_client.blpop('tasks', timeout=1)
        if task_data:
            _, task_json = task_data
            task = json.loads(task_json.decode('utf-8'))
            chat_id = task['chat_ids']
            message_text = task['message_text']
        else:
            # Если задач нет, ждем немного перед следующей проверкой
            await asyncio.sleep(1)


def clear_text(a):
    return re.sub(r"['\[\]()\,]", "", str(a))

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name} \n\n' '<i>Этот бот предназначен для отправки заданных '
                         'сообщений в ТОЛЬКО в группу по расписанию.\n\n'
                         'Для в заимодействия с ботом необходимо добавить его в группу и назначить администратором.</i>\n\n'
                         '<b><u>ЗАДАЧИ МОЖЕТ ВЫСТАВЛЯТЬ ТОЛЬКО АДМИНИСТРАТОР ЧАТА</u></b>',
                         parse_mode=types.ParseMode.HTML, disable_notification=True)


@dp.message_handler(commands="task")
async def task(message: types.Message):
    group = message.chat.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Работа с задачами", url=f"{os.getenv('URL_FRONT')}{group}", callback_data='copy_text'))
    # markup.add(types.InlineKeyboardButton("открыть страницу",web_app=WebAppInfo(url=f"https://perevyazko1.github.io/testprojectwebappbot/{group}")))
    await message.answer(f'Нажмите кнопку', reply_markup=markup,parse_mode=ParseMode.MARKDOWN)


@dp.message_handler()
async def handle_message(message: types.Message):
    modified_text = re.sub(r"(https://www\.)(instagram\.com/.+)", r"\1dd\2", message.text)
    if modified_text != message.text:
       await message.reply(modified_text)

# @dp.message_handler(commands="list_task")
# async def button_task(message: types.Message):
#     marcup = types.ReplyKeyboardMarkup()
#     marcup.add(types.KeyboardButton("открыть страницу", webapp="https://perevyazko1.github.io/botsenderfront"))



@dp.message_handler()
async def delete_command(message: types.Message):
    if message.text == '/start@CREATOR_TASK_FOR_CHAT_BOT' or message.text == '/task@CREATOR_TASK_FOR_CHAT_BOT' \
            or message.text == '/delete_task@CREATOR_TASK_FOR_CHAT_BOT' or message.text == '/list_task@CREATOR_TASK_FOR_CHAT_BOT':
        try:
            await message.delete()
        except MessageCantBeDeleted:
            await asyncio.sleep(1)

@dp.message_handler()
async def load_task(chat_id_group, text_task):
    print(text_task)
    try:
        await dp.bot.send_message(chat_id=chat_id_group, text=text_task)
        await asyncio.sleep(1)
    except BotKicked:
        await asyncio.sleep(1)

async def send_task():

    url = f"{os.getenv('SERVER_IP')}/app/get_all_task/"


    response = requests.get(url)

    if response.status_code == 200:
        sql_tasks = response.json()  # Парсинг JSON-данных, если ответ в формате JSON
        day_mapping = {
            'Ежедневно': aioschedule.every().day,
            'Понедельник': aioschedule.every().monday,
            'Вторник': aioschedule.every().tuesday,
            'Среда': aioschedule.every().wednesday,
            'Четверг': aioschedule.every().thursday,
            'Пятница': aioschedule.every().friday,
            'Суббота': aioschedule.every().saturday,
            'Воскресенье': aioschedule.every().sunday,
        }
        for task in sql_tasks:
            day_of_week = task.get('day_of_week')
            if day_of_week in day_mapping:
                day_mapping[day_of_week].at(time_str=str(task.get('time'))).do(load_task, task.get('chat_id'),
                                                                               task.get('task')).tag(f'{task.get("id")}')
            else:
                print(f"Unsupported day of the week: {day_of_week}")
    else:
        print('Request failed with status code:', response.status_code)
    while True:
        # Пытаемся получить задачу из Redis (блокирующий вызов с таймаутом в 1 секунду)
        create_tasks = redis_client.blpop('create_tasks', timeout=1)
        delete_tasks = redis_client.blpop('delete_tasks', timeout=1)
        day_mapping = {
            'Ежедневно': aioschedule.every().day,
            'Понедельник': aioschedule.every().monday,
            'Вторник': aioschedule.every().tuesday,
            'Среда': aioschedule.every().wednesday,
            'Четверг': aioschedule.every().thursday,
            'Пятница': aioschedule.every().friday,
            'Суббота': aioschedule.every().saturday,
            'Воскресенье': aioschedule.every().sunday,
        }

        if create_tasks:
            _, task_json = create_tasks
            task = json.loads(task_json.decode('utf-8'))
            day_of_week = task.get('day_of_week')
            print(task)
            day_mapping[day_of_week].at(time_str=str(task.get('time'))).do(load_task, task.get('chat_id'),
                                                                           task.get('task')).tag(f'{task.get("id")}')
        if delete_tasks:
            _, task_json = delete_tasks
            task = json.loads(task_json.decode('utf-8'))
            aioschedule.clear(f'{task.get("id")}')
        else:
            # Если задач нет, ждем немного перед следующей проверкой
            await asyncio.sleep(1)

        await aioschedule.run_pending()
        await asyncio.sleep(1)



async def on_startup(dp):
    asyncio.create_task(send_task())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
