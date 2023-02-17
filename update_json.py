import json


def read_json(json_path: str) -> list:
    """
    Read json file
    :param json_path: Path to json file
    :return: list with info from json
    """
    with open(json_path, 'r') as file:
        cont = json.load(file)
    return cont


def reset_list_info(json_path: str) -> None:
    """
    Reset all likes, dislikes for all pictures
    :param json_path: Path to json file
    :return: None
    """
    content = read_json(json_path)
    for item in content:
        item['likes'] = 0
        item['dislikes'] = 0
        item['liked-users'] = []
        item['disliked-users'] = []
    update_json(json_path, content)


def update_json(new_json_path, dict_list: list) -> None:
    """
    Update json file with new info
    :param new_json_path: path to json
    :param dict_list: Full photo items list with changed some info
    :return: None
    """
    with open(new_json_path, 'w') as file:
        json.dump(dict_list, file, indent=4, ensure_ascii=False)


def update_likes_json(photo_number: str, user_id: str) -> None:
    """
    Read json with items info. Find image by image number. Add like. Update json
    :param photo_number: Image number for updating
    :param user_id: User id which do this action
    :return: None
    """
    cont = read_json('data/content.json')
    for photo_item in cont:
        if photo_item['number'] == photo_number:
            photo_item['likes'] += 1
            photo_item['liked-users'].append(user_id)
            break
    update_json('data/content.json', cont)


def check_photo_rate(photo_number: str, user_id: str) -> bool:
    """
    Checking if the user has already rated the image
    :param photo_number: Image number for checking
    :param user_id: User id which do this action
    :return: True if User already rated the image, False - if user didn't rate the image
    """
    cont = read_json('data/content.json')
    for photo_item in cont:
        if photo_item['number'] == photo_number:
            return True if user_id in photo_item['liked-users'] or user_id in photo_item['disliked-users'] else False


def update_dislikes_json(photo_number: str, user_id: str) -> None:
    """
    Read json with items info. Find image by image number. Add dislike. Update json
    :param photo_number: Image number for updating
    :param user_id: User id which do this action
    :return: None
    """
    cont = read_json('data/content.json')
    for photo_item in cont:
        if photo_item['number'] == photo_number:
            photo_item['dislikes'] += 1
            photo_item['disliked-users'].append(user_id)
            break
    update_json('data/content.json', cont)

