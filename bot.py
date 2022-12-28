from asyncio import sleep

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.config import bot_token
from app.keyboards import dice_keyboard, play_again_keyboard

bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())


class OrderGame(StatesGroup):
    waiting_user_state = State()


@dp.message_handler(Text(equals='Play again 🎲'))
async def on_message(message: types.Message, state: FSMContext):

    await sleep(1)

    bot_data = await bot.send_dice(message.from_user.id)
    bot_data = bot_data['dice']['value']
    await state.update_data(bot_dice=bot_data)
    await OrderGame.waiting_user_state.set()
    await sleep(5)
    await message.answer('Now it\'s your turn to throw the dice! 🫵',
                         reply_markup=dice_keyboard)


@dp.message_handler(commands=['start', 'play'])
async def on_message(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.from_user.id,
        f'Hello, {message.from_user.username}!🫶 Let\'s play 😜'
    )
    await sleep(1)

    bot_data = await bot.send_dice(message.from_user.id)
    bot_data = bot_data['dice']['value']
    await state.update_data(bot_dice=bot_data)
    await OrderGame.waiting_user_state.set()
    await sleep(5)
    await message.answer('Now it\'s your turn to throw the dice! 🫵',
                         reply_markup=dice_keyboard)


@dp.message_handler(Text(equals='Throw the dice 🎲'),
                    state=OrderGame.waiting_user_state)
async def throw_the_dice(message: types.Message, state: FSMContext):
    user_data = await bot.send_dice(message.from_user.id,
                                    reply_markup=types.ReplyKeyboardRemove())
    user_data = user_data['dice']['value']
    await sleep(5)

    temp_data = await state.get_data()
    bot_data = temp_data['bot_dice']

    if bot_data > user_data:
        await bot.send_message(message.from_user.id, 'Sorry, you lose 🫠',
                               reply_markup=play_again_keyboard)
    elif bot_data < user_data:
        await bot.send_message(message.from_user.id, 'Wow, you won! 🏆',
                               reply_markup=play_again_keyboard)
    else:
        await bot.send_message(message.from_user.id, 'OMG 👀 We have a draw',
                               reply_markup=play_again_keyboard)

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp)
