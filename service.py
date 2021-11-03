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


def validation(login: str, password: str, phone_number: str) -> bool:
    if not login or not password or not phone_number:
        return False

    response = database.get_user_login(login)
    if not response:
        return False
    return True


def validation_update(id_: int, login: str, password: str, phone_number: str) -> bool:
    response = validation(login, password, phone_number)
    if not response:
        return False

    response = update_profile(id_, login, password, phone_number)
    return response


def update_profile(id_: int, login: str, password: str, phone_number: str) -> \
        bool:
    response = hash_password(password)
    response = database.update_profile(id_, login, response[0], response[1],
                                       phone_number)
    return response


def validation_signup(login: str, password: str, phone_number: str) -> bool:
    """Валидация введенных данных из формы регистрации"""
    response = validation(login, password, phone_number)
    if not response:
        return False

    response = create_new_user(login, password, phone_number)
    return response


def hash_password(password: str) -> list:
    salt = str(uuid4().int)
    hash = str(sha256((str(password + salt)).encode('utf-8')).hexdigest())
    response = [hash, salt]
    return response


def create_new_user(login: str, password: str, phone_number: str) -> bool:
    response = hash_password(password)
    response = database.create_user((login, response[0], response[1],
                                     phone_number))
    return response


def generate_new_pattern(title: str, id_: int, status: dict) -> bool:
    word_cloud, name_pattern = cloud.run(title)
    formatted_wc = '|'.join(word_cloud)
    response = database.add_pattern(name_pattern, formatted_wc, id_)
    status["success"] = True
    return response


def show_saved_pattern(id_: int) -> list:
    response = database.get_title_patterns(id_)
    return response


def generate_saved_pattern(title: str, status: dict) -> None:
    word_cloud = database.get_word_cloud_pattern(title)
    for i in word_cloud:
        word_cloud_formatted = i.split('|')
    cloud.run_saved_pattern(word_cloud_formatted)
    status["success"] = True
