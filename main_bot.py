import random
import json

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text

from keyboard import get_main_kb, get_picture_kb
from inline_keyboard import get_photo_inline_kb
from update_json import update_likes_json, update_dislikes_json, check_photo_rate

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

HELP_COMMAND_TEXT = """
<b>/start</b> - <em>Start bot</em>
<b>/help</b> - <em>list of commands</em>
<b>/picture</b> - <em>send a funny picture</em>
<b>/description</b> - <em>Bot description</em>
"""


async def on_startup(_):
    print('Bot start working...')


def get_photo_by_number(number: str) -> dict:
    """
    Get photo item from json file by given photo number
    :param number: photo number (matches the name)
    :return: dictionary with photo item
    """
    with open('data/content.json', 'r') as file:
        cont = json.load(file)
    for item in cont:
        if item["number"] == number:
            return item


def get_random_photo_info() -> dict:
    """
    Get random photo dict with info about the photo from json file
    :return: dict with random photo from json
    """
    with open('data/content.json', 'r') as file:
        cont = json.load(file)
    return random.choice(cont)


async def send_random_photo(message: types.Message) -> None:
    rand_photo = get_random_photo_info()
    picture = open(f'data/images/{rand_photo["number"]}.jpg', 'rb')
    await bot.send_photo(message.chat.id,
                         photo=picture,
                         caption='Do you like this photo??',
                         reply_markup=get_photo_inline_kb(rand_photo))


@dp.message_handler(Text(equals='Send me picture'))
async def send_photo(message: types.Message) -> None:
    await send_random_photo(message)
    await message.delete()


@dp.message_handler(Text(equals='Main menu'))
async def open_main_menu(message: types.Message) -> None:
    await message.answer('You in main menu!', reply_markup=get_main_kb())
    await message.delete()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
    await bot.send_message(message.chat.id, "Hello! I'm bot", reply_markup=get_main_kb())
    await message.delete()


@dp.message_handler(commands=['description'])
async def description_command(message: types.Message) -> None:
    await bot.send_message(message.chat.id, 'In this bot you can vote different pictures!')
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message) -> None:
    await bot.send_message(message.chat.id, HELP_COMMAND_TEXT, parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['pictures'])
async def random_picture(message: types.Message) -> None:
    await message.answer('If you want a picture - press button "Send me picture"', reply_markup=get_picture_kb())
    await message.delete()


@dp.callback_query_handler()
async def picture_callback(callback: types.CallbackQuery) -> None:
    # If the download button was pressed - send a photo
    if callback.data.split(' ')[0] == 'download':
        await callback.answer("I'll send you a photo")
        await bot.send_document(callback.message.chat.id, open(f'data/images/{callback.data.split(" ")[1]}.jpg', 'rb'))
    # If the like button was pressed - check likes and add like
    elif callback.data.split(' ')[0] == 'like':
        photo_number = callback.data.split(' ')[1]
        if check_photo_rate(photo_number, callback.from_user.id):  # check if the user has rated the photo
            await callback.answer('You have already rated the photo!')
        else:
            update_likes_json(photo_number, callback.from_user.id)
            await callback.message.edit_reply_markup(
                reply_markup=get_photo_inline_kb(get_photo_by_number(photo_number)))
            await callback.answer('You like this photo!')

    # If the dislike button was pressed - check dislikes and add dislike
    elif callback.data.split(' ')[0] == 'dislike':
        photo_number = callback.data.split(' ')[1]
        if check_photo_rate(photo_number, callback.from_user.id):  # check if the user has rated the photo
            await callback.answer('You have already rated the photo!')
        else:
            update_dislikes_json(photo_number, callback.from_user.id)
            await callback.message.edit_reply_markup(
                reply_markup=get_photo_inline_kb(get_photo_by_number(photo_number)))
            await callback.answer('You dislike this photo!')
    # Next photo
    else:
        await callback.answer('Next photo!')
        await send_random_photo(callback.message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
