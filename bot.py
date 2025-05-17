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

basical_val_k = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='RUB', callback_data='RUB'),
        InlineKeyboardButton(text='USD', callback_data='USD')
    ]
])

async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет! Выбери,пожалуйста,базовую валюту:\n(если не понятно,что такое базовая влюта напиши /help)', reply_markup=basical_val_k)
    await state.set_state(Form.basic_val)

@dp.message(F.text == '/help')
async def help_basval(message: Message):
    await message.answer('Базовая валюта - это валюта в которой будет исчисляться цена других валют.')


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.message.register(start, F.text == '/start')
    dp.message.register(help_basval, F.text == '/help')

    await dp.start_polling(bot)

asyncio.run(main())
