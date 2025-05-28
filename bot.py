from topvalues import valsx
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

API_TOKEN = ''
# Convert bot

usd = [[30,30.3,31,31.8,41.8,60.7,66.9,58,62.6,64.73,75.2,71,80,93,97.25],[0.03,0.03,0.03,0.03,0.02,0.02,0.01,0.02,0.01,0.01,0.01,0.01,0.01,0.01,0.01]]

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class Form(StatesGroup):
    basic_val = State()
    action = State()
    valkrs = State()
    valconvert = State()
    hm = State()
    yn = State()
    noitca = State()
    valkrs2 = State()
    year = State()
    valconvert2 = State()
    hm2 = State()
    year2 = State()


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

choose_choose_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Да', callback_data='Да'),
        InlineKeyboardButton(text='Не', callback_data='Не')
    ]
])


@dp.message(F.text == '/start')
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет! Выбери, пожалуйста, базовую валюту:\n(если не понятно, что такое базовая валюта, напиши /help)', 
                        reply_markup=basical_val_k)
    await state.set_state(Form.basic_val)


@dp.message(F.text == '/help')
async def help_basval(message: Message):
    await message.answer('Базовая валюта - валюта, за единицу которой будет выводиться цена в выбранной валюте '
                        '(выбрана базовая валюта USD, курс RUB = 80RUB за 1 USD)')


@dp.callback_query(F.data.in_(["RUB", "USD"]), Form.basic_val)
async def choose_yn(callback: CallbackQuery, state: FSMContext):
    await state.update_data(basic_val=callback.data)
    await callback.message.answer('Конвертировать/узнать курс за период с 2010-2024?', 
                                reply_markup=choose_choose_kb)
    await state.set_state(Form.yn)
    await callback.answer()


@dp.callback_query(F.data == 'Не', Form.yn)
async def choose_action(callback: CallbackQuery, state: FSMContext):
    await state.update_data(yn=callback.data)
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
async def hmconvert(callback: CallbackQuery, state: FSMContext):
    await state.update_data(action='Конвертировать валюту')
    await callback.message.answer('Напиши сколько нужно конвертировать валюты:')
    await state.set_state(Form.hm)
    await callback.answer()


@dp.message(Form.hm)
async def valforconvert(message: Message, state: FSMContext):
    try:
        hm = float(message.text)
        await state.update_data(hm=hm)
        await message.answer('Напиши валюту в формате описанном по ссылке: \n https://www.exchangerate-api.com/docs/supported-currencies')
        await state.set_state(Form.valconvert)
    except ValueError:
        await message.answer('Пожалуйста, введите число!')


@dp.message(Form.valconvert)
async def convert(message: Message, state: FSMContext):
    data = await state.get_data()
    basic_val = data.get('basic_val')
    hm = float(data.get('hm'))
    valconvert = message.text
    c = valsx(basic_val, valconvert)
    await message.answer(f'{hm} {valconvert} = {c * hm} {basic_val}')
    await state.clear()


@dp.callback_query(F.data == 'Да', Form.yn)
async def choose_action2(callback: CallbackQuery, state: FSMContext):
    await state.update_data(yn=callback.data)
    await callback.message.answer("Выбери нужное действие:", reply_markup=choose_action_kb)
    await state.set_state(Form.noitca)
    await callback.answer()


@dp.callback_query(F.data == 'Узнать курс', Form.noitca)
async def valpr2(callback: CallbackQuery, state: FSMContext):
    await state.update_data(action='Узнать курс')
    await callback.message.answer('Введите валюту,чей курс хотите узнать в нужном формате:\n Российский рубль(RUB)\n Доллар США(USD)\n Евро(EUR)')
    await state.set_state(Form.valkrs2)
    await callback.answer()


@dp.message(Form.valkrs2)
async def yearw(message: Message, state: FSMContext):
    await state.update_data(valkrs2=message.text)
    await message.answer('Хорошо!\nТеперь введите цифру 0-14, где\n0-2010 год\n14-2024 год')
    await state.set_state(Form.year)


@dp.message(Form.year)
async def krs(message: Message, state: FSMContext):    
    await state.update_data(year=message.text)        
    data = await state.get_data()
    valkrs2 = data.get('valkrs2')
    basval = data.get('basic_val')
    year = data.get('year')
    if valkrs2 == 'USD':
        if basval == 'RUB': result = usd[0][int(year)]
        else:result = usd[1][int(year)]
        await message.answer(f'Курс {valkrs2} к {basval} в {2010 + int(year)} году: {result}')
    await state.clear()
        
@dp.callback_query(F.data == 'Конвертировать валюту', Form.noitca)
async def val(callback: CallbackQuery, state: FSMContext):
    await state.update_data(noitca='Конвертировать валюту')
    await callback.message.answer('Введите валюту,которую хотите конвертировать в нужном формате:\n Российский рубль(RUB)\n Доллар США(USD)\n Евро(EUR)')
    await state.set_state(Form.valconvert2)
    await callback.answer()

@dp.message(Form.valconvert2)
async def hmc(message:Message, state):
    await state.update_data(valconvert2=message.text)
    await message.answer('Сколько валюты конвертировать?')
    await state.set_state(Form.hm2)

@dp.message(Form.hm2)
async def yearwrite(message: Message, state: FSMContext):
    await state.update_data(hm2=message.text)
    await message.answer('Хорошо!\nТеперь введите цифру 0-14, где\n0-2010 год\n14-2024 год')
    await state.set_state(Form.year2)

@dp.message(Form.year2)
async def convert2(message: Message, state: FSMContext):
    data = await state.get_data()
    basic_val = data.get('basic_val')
    hm2 = int(data.get('hm2'))
    year2 = int(message.text)
    val = data.get('valconvert2')
    if basic_val == val:
        await message.answer('Мне кажется, вы уже знаете ответ;)')
        await state.clear()
    else:
        if val == 'USD':
            if basic_val == 'RUB': await message.answer(f'{hm2} {val} = {usd[0][year2] * hm2} {basic_val}')
            else: await message.answer(f'{hm2} {val} = {usd[1][year2] * hm2} {basic_val}')
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
    dp.message.register(choose_yn,Form.basic_val)
    dp.message.register(choose_action2,Form.yn)
    dp.message.register(valpr2,Form.noitca)
    dp.message.register(yearw,Form.valkrs2)
    dp.message.register(krs,Form.year)
    dp.message.register(val,Form.noitca)
    dp.message.register(hmc,Form.valconvert2)
    dp.message.register(yearwrite,Form.hm2)
    dp.message.register(convert2,Form.year2)

    await dp.start_polling(bot)

asyncio.run(main())

