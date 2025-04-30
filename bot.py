import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from aiogram.utils.keyboard import InlineKeyboardBuilder
from text import Days
import datetime
import time


# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
week = '1_week'
message_id = []
last_set_date = None
current_index = -1
current_value = None
is_first_run = True 



async def days_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Понедельник", callback_data="monday")
    kb.button(text="Вторник", callback_data="tuesday")
    kb.button(text="Среда", callback_data="wednesday")
    kb.button(text="Четверг", callback_data="thursday")
    kb.button(text="Пятница", callback_data="friday")
    kb.button(text="Суббота", callback_data="saturday")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

async def back_kb(message_id):
    kb = InlineKeyboardBuilder()
    kb.button(text="Назад", callback_data=f"back:{message_id}")
    return kb.as_markup(resize_keyboard=True)


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if week == "1_week":
        week_now = 'первая неделя'

    if week == '2_week':
        week_now = 'вторая неделя'
    await message.answer(text = f'Сегодня {week_now}\n Выбери день', reply_markup = await days_kb())

# Обработчик текстовых сообщений


@dp.callback_query(F.data == "monday")
async def mondey(callback: types.CallbackQuery):
    a = await callback.message.edit_text(text="Расписание на понедельник")
    await callback.message.answer(text=Days.MONDEY_ONE_WEEK, reply_markup = await back_kb(a.message_id))
    message_id.append(a.message_id)
    
@dp.callback_query(F.data == "tuesday")
async def tuesday(callback: types.CallbackQuery):
    a = await callback.message.edit_text(text="Расписание на вторник")
    await callback.message.answer(text=Days.TUESDAY_ONE_WEEK, reply_markup = await back_kb(a.message_id))
    


@dp.callback_query(F.data == "wednesday")
async def wednesday(callback: types.CallbackQuery):

    
    a = await callback.message.edit_text(text="Расписание на среду")
    if week == '1_week':
        await callback.message.answer(text=Days.WEDNESDAY_ONE_WEEK, reply_markup = await back_kb(a.message_id))
        
    if week == '2_week':
        await callback.message.answer(text=Days.WEDNESDAY_TWO_WEEK, reply_markup = await back_kb(a.message_id))
    
    
    

@dp.callback_query(F.data == "thursday")
async def thursday(callback: types.CallbackQuery):
    a = await callback.message.edit_text(text="Расписание на четверг")
    if week == '1_week':
        await callback.message.answer(text=Days.THURSDAY_ONE_WEEK, reply_markup = await back_kb(a.message_id))
        
    if week == '2_week':
        await callback.message.answer(text=Days.THURSDAY_TWO_WEEK, reply_markup = await back_kb(a.message_id))
        

@dp.callback_query(F.data == "friday")
async def friday(callback: types.CallbackQuery):
    a = await callback.message.edit_text(text="Расписание на пятницу")
    if week == '1_week':
        await callback.message.answer(text=Days.FRIDAY_ONE_WEEK, reply_markup = await back_kb(a.message_id))
        
    if week == '2_week':
        await callback.message.answer(text=Days.FRIDAY_TWO_WEEK, reply_markup = await back_kb(a.message_id))
    


@dp.callback_query(F.data == "saturday")
async def saturday(callback: types.CallbackQuery):
    a = await callback.message.edit_text(text="Расписание на субботу")
    if week == '1_week':
        await callback.message.answer(text=Days.SATURDAY_ONE_WEEK, reply_markup = await back_kb(a.message_id))
    if week == '2_week':
        await callback.message.answer(text=Days.SATURDAY_TWO_WEEK, reply_markup = await back_kb(a.message_id))   
    
    
    message_id.append(a.message_id)

@dp.callback_query(F.data.startswith("back:"))
async def back(callback: types.CallbackQuery):

    message_id = callback.data.split(":")[1]
    await callback.message.delete()
   
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=message_id)
    if week == "1_week":
        week_now = 'первая неделя'

    if week == '2_week':
        week_now = 'вторая неделя'
    await callback.message.answer(text = f'Сегодня {week_now}\nВыбери день', reply_markup = await days_kb())
    


def is_sunday(date):
    return date.weekday() == 6  # 6 = воскресенье

def toggle_week(current):
    return '2_week' if current == '1_week' else '1_week'

 
async def refresh():
  global week, last_set_date
  while True:
    today = datetime.date.today()
    
    
    if is_sunday(today):
        if last_set_date != today:
            # Если сегодня воскресенье и мы ещё не обновляли значение — переключаем
            week = toggle_week(week)   # если первый запуск
            last_set_date = today
            print(f"[{datetime.datetime.now()}] Воскресенье: week = {week}")
        else:
            print(f"[{datetime.datetime.now()}] Уже установлено на сегодня: week = {week}")
    else:
        print(f"[{datetime.datetime.now()}] Не воскресенье: week = {week}")
    
    await asyncio.sleep(26100)  # Проверка каждые 12 часов






# Запуск бота
async def main():
    asyncio.create_task(refresh())
    await dp.start_polling(bot)
  

if __name__ == "__main__":
    asyncio.run(main()) 


