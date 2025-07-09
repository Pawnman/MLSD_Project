from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
import joblib

Moscow = pd.read_csv('flats_Moscow.csv')
Ekat = pd.read_csv('flats_Ekat.csv')
Kazan = pd.read_csv('flats_Kazan.csv')
Novosib = pd.read_csv('flats_Novosib.csv')
SaintP = pd.read_csv('flats_SaintP.csv')

async def filter(city_df,data, price, message):
    links = city_df[(city_df['price_per_month'] >= price - 10000) & (city_df['price_per_month'] <= price + 10000) &
                   (city_df['rooms_count'] == int(data['rooms_count'])) & (city_df['city'] == data['city']) & (
                               city_df['total_meters'] >= int(data['total_meters']) - 10) &
                   (city_df['total_meters'] <= int(data['total_meters']) + 10) & (
                               city_df['underground'] == data['underground'])]['link']

    if len(links) == 0:
        await bot.send_message(message.from_user.id, f'По твоему запросу ничего не найдено, уточни запрос!')
    else:
        await bot.send_message(message.from_user.id, f'По твоему запросу могу предложить следующие варианты:')
        for i in links:
            await bot.send_message(message.from_user.id, f'{i}')

    print(links)
    print(data['city'], int(data['floor']), int(data['floor_count']), int(data['rooms_count']),
          int(data['total_meters']), data['underground'])


loaded_model = joblib.load('modelpipelinefinal.pickle')

TOKEN = "6819265433:AAFqrG_l0jCZTPG1UII5VbW_4xNWPfx9Dvo"

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

def city_buttons():
    markup = InlineKeyboardMarkup()
    city1 = InlineKeyboardButton(text='Москва', callback_data='Москва')
    city2 = InlineKeyboardButton(text='Санкт-Петербург', callback_data='Санкт-Петербург')
    city3 = InlineKeyboardButton(text='Казань', callback_data='Казань')
    city4 = InlineKeyboardButton(text='Екатеринбург', callback_data='Екатеринбург')
    city5 = InlineKeyboardButton(text='Новосибирск', callback_data='Новосибирск')
    markup.add(city1, city2, city3, city4, city5)
    return markup
def buttons():
    markup = InlineKeyboardMarkup()
    floor1 = InlineKeyboardButton(text='1', callback_data=1)
    floor2 = InlineKeyboardButton(text='2', callback_data=2)
    floor3 = InlineKeyboardButton(text='3', callback_data=3)
    floor4 = InlineKeyboardButton(text='4', callback_data=4)
    markup.add(floor1, floor2, floor3,floor4)
    return markup

class FlatInfo(StatesGroup):
    CITY = State()
    FLOOR = State()
    FLOORS_COUNT = State()
    ROOMS_COUNT = State()
    TOTAL_METERS = State()
    UNDERGROUND = State()
    SCORE = State()




@dp.message_handler(commands=['start'])
async def ask_FLOOR(message, state):
    await bot.send_message(message.chat.id,
                           'Привет! Я умный бот, который поможет тебе сориентироваться в стоимости аренды квартир')
    await bot.send_message(message.chat.id, 'Введи город в котором ты ищешь квартиру',
                           reply_markup=city_buttons())
    await state.set_state(FlatInfo.CITY)



@dp.callback_query_handler(state= FlatInfo.CITY)
async def rooms_buttons(call, state):
    await call.answer()
    await state.update_data(city=call.data)
    await bot.send_message(call.from_user.id, 'Введи этаж')
    await state.set_state(FlatInfo.FLOOR)

@dp.message_handler(state = FlatInfo.FLOOR)
async def ask_FLOOR(message, state):
    await state.update_data(floor=message.text)
    await bot.send_message(message.chat.id, 'Введи количество этажей в доме')
    await state.set_state(FlatInfo.FLOORS_COUNT)


@dp.message_handler(state = FlatInfo.FLOORS_COUNT)
async def ask_FLOOR(message, state):
    await state.update_data(floor_count=message.text)
    await bot.send_message(message.chat.id, 'Введи желаемое количество комнат в квартире', reply_markup=buttons())
    await state.set_state(FlatInfo.ROOMS_COUNT)


@dp.callback_query_handler(state= FlatInfo.ROOMS_COUNT)
async def rooms_buttons(call, state):
    await call.answer()
    await state.update_data(rooms_count=call.data)
    await bot.send_message(call.from_user.id, 'Введи количество метров в квартире')
    await state.set_state(FlatInfo.TOTAL_METERS)


@dp.message_handler(state=FlatInfo.TOTAL_METERS)
async def ask_FLOOR(message, state):
    await state.update_data(total_meters=message.text)
    await bot.send_message(message.chat.id, 'Введи метро')
    await state.set_state(FlatInfo.UNDERGROUND)

@dp.message_handler(state=FlatInfo.UNDERGROUND)
async def ask_FLOOR(message, state):
    await state.update_data(underground=message.text)
    data = await state.get_data()

    test = pd.DataFrame([[0, data['city'], int(data['floor']), int(data['floor_count']), int(data['rooms_count']), int(data['total_meters']), data['underground']]],
                        columns=["Unnamed: 0", "city", "floor", "floors_count", "rooms_count", "total_meters",
                                 "underground"])

    price = loaded_model.predict(test)[0]
    await bot.send_message(message.chat.id, "Ориентировочная стоимость аренды квартиры по твоим параметрам: " + str(round(price)))
    if data['city'] == 'Москва':
        await filter(Moscow,data, price, message)
    if data['city'] == 'Санкт-Петербург':
        await filter(SaintP,data, price, message)
    if data['city'] == 'Казань':
        await filter(Kazan, data, price, message)
    if data['city'] == 'Новосибирск':
        await filter(Novosib,data, price, message)
    if data['city'] == 'Екатеринбург':
        await filter(Ekat, data, price, message)

    await state.set_state(FlatInfo.SCORE)
    await bot.send_message(message.chat.id, "Помоги мне стать лучше, оцени мою работу по десятибалльной шкале")

@dp.message_handler(state=FlatInfo.SCORE)
async def ask_FLOOR(message, state):
    await state.update_data(score=message.text)
    df = pd.read_csv('score.csv')
    df.loc[len(df.index)] = [message.chat.id, message.text]
    df.to_csv('score.csv', index = False)
    await bot.send_message(message.chat.id, "Спасибо, твой отзыв учтён!",reply_markup=types.ReplyKeyboardMarkup().add(types.KeyboardButton('/start')))
    await state.finish()

executor.start_polling(dp)