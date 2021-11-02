from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel

import database
import service
import main_screen


class Authorization(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setFixedSize(500, 530)

    def initUI(self):
        # Инфо текст
        self.text = QLabel(self)
        self.text.setText("Введите данные для регистрации")
        self.text.move(20, 55)
        self.text.setStyleSheet('.QLabel { font-size: 20pt; font-weight: '
                                'Bold }')

        # Кнопка регистрации
        self.btn = QPushButton('Зарегистрироваться', self)
        self.btn.resize(280, 55)
        self.btn.move(110, 384)
        self.btn.setStyleSheet('.QPushButton { font-size: 15pt; }')
        self.btn.clicked.connect(self.validation_data)

        # Форма для пароля
        self.password = QLineEdit(self)
        self.password.resize(400, 50)
        self.password.move(50, 294)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText('Пароль')

        # Форма для логина
        self.login = QLineEdit(self)
        self.login.resize(400, 50)
        self.login.move(50, 219)
        self.login.setPlaceholderText('Логин')

        # Форма для номера телефона
        self.phone_number = QLineEdit(self)
        self.phone_number.resize(400, 50)
        self.phone_number.move(50, 144)
        self.phone_number.setPlaceholderText('Номер телефона')
        self.phone_number.setInputMask("+7 (000) 000 00 00")

        # Параметры окна
        self.setWindowTitle('WordPatterns')
        self.show()

    def validation_data(self):
        phone_number = self.phone_number.text()
        login = self.login.text()
        password = self.password.text()

        response = service.validation_signup(login, password, phone_number)

        if not response:
            return QtWidgets.QMessageBox.warning(self, 'Ошибка',
                                                 'Неверные данные! Возможно, '
                                                 'такой логин уже занят!')

        id_ = database.get_user_id(login)

        return self.open_main_widget(id_)

    def open_main_widget(self, id_):
        """Открываем новый виджет"""
        self.main_screen = main_screen.MainScreen(id_)
        self.main_screen.show()
        self.close()
