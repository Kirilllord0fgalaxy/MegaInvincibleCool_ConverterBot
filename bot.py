from topvalues import valsx
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

API_TOKEN=''
#Convert bot

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class Form(StatesGroup):
    basic_val = State()
    action = State()
    valkrs = State()
    valconvert = State()
    hm = State()

basical_val_k = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='RUB', callback_data='RUB'),
        InlineKeyboardButton(text='USD', callback_data='USD')
    ]
])

choose_action_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Узнать курс', callback_data='Узнать курс'),
        InlineKeyboardButton(text='Конвертировать валюту', callback_data='Конвертировать валюту')
    ]
])

async def start(message: Message, state):
    await state.clear()
    await message.answer('Привет! Выбери,пожалуйста,базовую валюту:\n(если не понятно,что такое базовая влюта напиши /help)', reply_markup=basical_val_k)
    await state.set_state(Form.basic_val)

@dp.message(F.text == '/help')
async def help_basval(message: Message):
    await message.answer('Базовая валюта - валюта за единицу которой будет выводится цена в выбранной валюте(выбрана базовая валюта USD, курс RUB = 80RUB за 1 USD)')

@dp.callback_query(lambda c: c.data in ["RUB", "USD"])
async def choose_action(callback: CallbackQuery, state):
    await state.update_data(basic_val=callback.data)
    await callback.message.answer("Выбери нужное действие:", reply_markup=choose_action_kb)
    await state.set_state(Form.action)
    await callback.answer()

@dp.callback_query(F.data == 'Узнать курс', Form.action)
async def valpr(callback: CallbackQuery, state: FSMContext):
    await state.update_data(action='Узнать курс')
    await callback.message.answer('Напиши валюту в формате описанном по ссылке: \n https://www.exchangerate-api.com/docs/supported-currencies')
    await state.set_state(Form.valkrs)
    await callback.answer()

@dp.message(Form.valkrs)
async def krsval(message: Message, state: FSMContext):
    data = await state.get_data()
    basic_val = data.get('basic_val')
    val = message.text
    a = valsx(val, basic_val)
    await message.answer(f'Курс {val}: {a} за 1 {basic_val}')
    await state.clear()

@dp.callback_query(F.data == 'Конвертировать валюту', Form.action)
async def hmconvert(callback:CallbackQuery, state:FSMContext):
    await state.update_data(action='Конвертировать валюту')
    await callback.message.answer('Напиши сколько нужно конвертировать валюты:')
    await state.set_state(Form.hm)

@dp.message(Form.hm)
async def valforconvert(message:Message, state: FSMContext):
    await state.update_data(hm=message.text)
    await state.set_state(Form.valconvert)
    await message.answer('Напиши валюту в формате22 описанном по ссылке: \n https://www.exchangerate-api.com/docs/supported-currencies')

@dp.message(Form.valconvert)
async def convert(message:Message, state: FSMContext):
    await state.update_data(valconvert=message.text)
    data = await state.get_data()
    basic_val = data.get('basic_val')
    hm = int(data.get('hm'))
    valconvert = data.get('valconvert')
    c = valsx(basic_val,valconvert)
    print(c,valconvert, basic_val)
    await message.answer(f'{hm}{valconvert} = {c*hm}{basic_val}')
    await state.clear()


async def main():
    dp.message.register(start, F.text == '/start')
    dp.message.register(help_basval, F.text == '/help')
    dp.message.register(choose_action,Form.action)
    dp.message.register(valpr,Form.valkrs)
    dp.message.register(krsval,Form.valkrs)
    dp.message.register(hmconvert,Form.hm)
    dp.message.register(valforconvert,Form.hm)
    dp.message.register(convert,Form.valconvert)

    await dp.start_polling(bot)

asyncio.run(main())

