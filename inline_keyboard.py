from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_photo_inline_kb(photo_dict: dict) -> InlineKeyboardMarkup:
    """
    Inline keyboard for photo cards
    :param photo_dict: photo item from json db with photo info
    :return: Inline keyboard
    """
    photo_inline_kb = InlineKeyboardMarkup(row_width=2)
    photo_like_button = InlineKeyboardButton(text=f'❤️ {photo_dict["likes"]}', callback_data=f'like {photo_dict["number"]}')
    photo_dislike_button = InlineKeyboardButton(text=f'💩 {photo_dict["dislikes"]}', callback_data=f'dislike {photo_dict["number"]}')
    photo_next_pick_button = InlineKeyboardButton(text='Next picture', callback_data='next')
    photo_download_button = InlineKeyboardButton(text='Download', callback_data=f'download {photo_dict["number"]}')

    photo_inline_kb.add(photo_like_button, photo_dislike_button).add(photo_next_pick_button).add(photo_download_button)

    return photo_inline_kb
