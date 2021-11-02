from uuid import uuid4
from hashlib import sha256

import database
import cloud


def validation_signin(login: str, password: str) -> bool:
    """Валидация введенных данных из формы входа"""
    if login == '' or password == '':
        return False
    response = database.get_user_data(login)

    if not response:
        return False

    if response[0] == \
            sha256((str(password + response[1])).encode('utf-8')).hexdigest():
        return True
    else:
        return False


def validation_signup(login: str, password: str, phone_number: str) -> bool:
    """Валидация введенных данных из формы регистрации"""
    if not login or not password or not phone_number:
        return False

    response = database.get_user_login(login)
    if not response:
        return False
    response = create_new_user(login, password, phone_number)
    return response


def create_new_user(login: str, password: str, phone_number: str) -> bool:
    salt = str(uuid4().int)
    hash = str(sha256((str(password + salt)).encode('utf-8')).hexdigest())

    response = database.create_user((login, hash, salt, phone_number))
    return response


def generate_new_pattern(title: str, id_: int) -> bool:
    word_cloud, name_pattern = cloud.run(title)
    formatted_wc = '|'.join(word_cloud)
    response = database.add_pattern(name_pattern, formatted_wc, id_)
    return response


def show_saved_pattern(id_: int) -> list:
    response = database.get_title_patterns(id_)
    return response


def generate_saved_pattern(title: str) -> None:
    word_cloud = database.get_word_cloud_pattern(title)
    for i in word_cloud:
        word_cloud_formatted = i.split('|')
    cloud.run_saved_pattern(word_cloud_formatted)
