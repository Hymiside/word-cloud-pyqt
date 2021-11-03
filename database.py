import sqlite3
from typing import Tuple

conn = sqlite3.connect("service.db", check_same_thread=False)
cursor = conn.cursor()


def create_user(values: Tuple) -> bool:
    """Добавление нового пользователя в БД"""
    try:
        cursor.execute(f"INSERT INTO users(login, hash, salt, phone) "
                       f"VALUES(?, ?, ?, ?);", values)
        conn.commit()
        return True
    except sqlite3.Error:
        return False


def get_user_data(login: str) -> list:
    """Достаем hash и salt для аутентификации"""
    cursor.execute("SELECT hash, salt FROM users WHERE login = ?", (login, ))
    list_ = cursor.fetchall()

    if not list_:
        return []
    data = [ii for i in list_ for ii in i]
    return data


def get_user_login(login: str) -> bool:
    """Достаем логин пользователя для проверка на наличие пользователя в БД"""
    cursor.execute("SELECT login FROM users WHERE login = ?", (login, ))
    response = cursor.fetchall()

    if response:
        return False
    return True


def get_user_id(login: str) -> int:
    """Возвращает id пользователя для имитации сессии"""
    cursor.execute("SELECT id FROM users WHERE login = ?", (login, ))
    tuple_ = cursor.fetchone()
    for i in tuple_:
        id_ = i
    return id_


def add_pattern(title: str, word_cloud: str, user_id: int) -> bool:
    """Добавляет в БД новый паттерн"""
    try:
        cursor.execute("INSERT INTO patterns(title, word_cloud, user_id) "
                       "VALUES(?, ?, ?);", (title, word_cloud, user_id))
        conn.commit()
        return True
    except sqlite3.Error:
        return False


def get_title_patterns(id_: int) -> list:
    """Достает все тайтлы паттернов пользователя"""
    cursor.execute("SELECT title FROM patterns WHERE user_id = ?", (id_, ))
    list_title = [ii for i in cursor.fetchall() for ii in i]
    return list_title


def get_word_cloud_pattern(title: str) -> list:
    """Возвращает облако слов по названию"""
    cursor.execute("SELECT word_cloud FROM patterns WHERE title = ?", (title, ))
    word_cloud = [i for i in cursor.fetchone()]
    return word_cloud


def update_profile(id_: int, login: str, hash: str, salt: str, phone: str) \
        -> bool:
    """Обновляет данные пользователя"""
    try:
        cursor.execute("UPDATE users SET login = ?, hash = ?, salt = ?, "
                       "phone = ? WHERE id = ?",
                       (login, hash, salt, phone, id_))
        conn.commit()
        return True
    except sqlite3.Error:
        return False


def init_db():
    """Инициализирует БД"""
    with open("createtb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT * FROM sqlite_master")
    table_exists = cursor.fetchall()

    if not table_exists:
        init_db()


check_db_exists()
