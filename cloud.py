import json
import random
import string
import uuid
from collections import Counter
from typing import List
import pymorphy2
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud

sw = set(stopwords.words('russian'))
table = str.maketrans(dict.fromkeys(string.punctuation))
stopgramms = ['NPRO', 'PREP', 'CONJ', 'PRCL', 'INTJ']
morph = pymorphy2.MorphAnalyzer(lang='ru')


# Читаем json переписки из телеграма и конвертируем его в тип dict
def read_json_tg() -> List[dict]:
    with open("result.json", encoding="utf-8", errors="ignore") as a:
        load_chat = [json.load(a)]
        return load_chat


# Считываем все данные типа messages
def get_messages(load_chat):
    for item in load_chat:
        if type(item) is dict:
            messages = item["messages"]
            return messages
    return []


# Чистим сообщения от не нужных знаков
def process(source: List[dict]) -> List[list]:
    messages = [normalize(read_message(message))
                for message in source if validation_message(message)]
    return messages


# Валидация сообщений
def validation_message(obj: dict) -> bool:
    if obj.get('type') != 'message':
        return False

    message_text = obj.get('text')
    response = type(message_text) is str and message_text != ''
    return response


# Читаем текст из сообщения
def read_message(obj: dict) -> str:
    message_text = obj.get('text')
    return message_text


# Убираем знаки пунктуации, союзы, предлоги
def normalize(text: str) -> [str]:
    text_with_punctuation = text.translate(table)
    tokens = []

    for w in word_tokenize(text_with_punctuation):
        p = morph.parse(w)[0]
        if p.tag.POS not in stopgramms:
            tokens.append(w)

    filtered_text = [w.lower() for w in tokens if not w.lower()
                     in sw and not w.isdigit()]
    return filtered_text


# Собираем список из всех слов переписки
def create_word_list(data: [[str]]) -> [str]:
    word_list = [item for sub in data for item in sub if len(item) != 0]
    return word_list


# Генерируем облако слов из списка слов переписки и создаем паттерн
def generate_cloud(word_list: [str], name_pattern: str) -> None:
    freq = Counter(word_list)

    if not name_pattern:
        name_pattern = str(uuid.uuid4())[:7]

    wc = WordCloud(width=1920, height=1080, max_words=20000, margin=10,
                   random_state=1).generate_from_frequencies(freq)
    plt.imshow(wc.recolor(random_state=int(random.random() * 256)),
               interpolation="bilinear")
    wc.to_file(name_pattern + '.png')
    plt.show()


def run(name_pattern: str) -> list and str:
    source = read_json_tg()
    user_chat = get_messages(source)
    processed_data = process(user_chat)
    data = create_word_list(processed_data)
    generate_cloud(data, name_pattern)

    return data, name_pattern


def run_saved_pattern(word_cloud: list) -> None:
    generate_cloud(word_cloud, "")

