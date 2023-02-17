from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_kb() -> ReplyKeyboardMarkup:
    """
    Get keyboard for main menu
    :return: ReplyKeyboardMarkup
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    start_button = KeyboardButton('/start')
    help_button = KeyboardButton('/help')
    description_button = KeyboardButton('/description')
    pictures_button = KeyboardButton('/pictures')

    kb.add(start_button, help_button).add(description_button, pictures_button)

    return kb


def get_picture_kb() -> ReplyKeyboardMarkup:
    """
    Get keyboard for pictures
    :return: ReplyKeyboardMarkup
    """
    picture_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu_button = KeyboardButton('Main menu')
    send_photo_button = KeyboardButton('Send me picture')
    picture_kb.add(send_photo_button, main_menu_button)
    return picture_kb
