from aiogram import types

dice_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
throw_button = types.KeyboardButton(text='Throw the dice 🎲')
dice_keyboard.add(throw_button)

play_again_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                one_time_keyboard=True)
play_again_button = types.KeyboardButton(text='Play again 🎲')
play_again_keyboard.add(play_again_button)
