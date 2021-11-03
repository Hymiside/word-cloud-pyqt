from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel

import service
import main_screen


class UpdateProfile(QWidget):

    def __init__(self, id_):
        super().__init__()

        self.id_ = id_

        self.initUI()
        self.setFixedSize(500, 530)

    def initUI(self):
        # Инфо текст
        self.text = QLabel(self)
        self.text.setText("Введите новые данные\nдля редактирования")
        self.text.move(50, 55)
        self.text.setStyleSheet('.QLabel { font-size: 20pt; font-weight: '
                                'Bold }')

        # Кнопка регистрации
        self.btn = QPushButton('Сохранить', self)
        self.btn.resize(220, 45)
        self.btn.move(50, 410)
        self.btn.setStyleSheet('.QPushButton { font-size: 13pt; }')
        self.btn.clicked.connect(self.validation_data)

        self.btn = QPushButton('Назад', self)
        self.btn.resize(150, 45)
        self.btn.move(300, 410)
        self.btn.setStyleSheet('.QPushButton { font-size: 13pt; }')
        self.btn.clicked.connect(self.back)

        # Форма для пароля
        self.password = QLineEdit(self)
        self.password.resize(400, 50)
        self.password.move(50, 314)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText('Пароль')

        # Форма для логина
        self.login = QLineEdit(self)
        self.login.resize(400, 50)
        self.login.move(50, 244)
        self.login.setPlaceholderText('Логин')

        # Форма для номера телефона
        self.phone_number = QLineEdit(self)
        self.phone_number.resize(400, 50)
        self.phone_number.move(50, 174)
        self.phone_number.setPlaceholderText('Номер телефона')
        self.phone_number.setInputMask("+7 (000) 000 00 00")

        # Параметры окна
        self.setWindowTitle('WordPatterns')
        self.show()

    def validation_data(self):
        phone_number = self.phone_number.text()
        login = self.login.text()
        password = self.password.text()

        response = service.validation_update(self.id_, login, password,
                                             phone_number)

        if not response:
            return QtWidgets.QMessageBox.warning(self, 'Ошибка',
                                                 'Неверные данные! Возможно, '
                                                 'такой логин уже занят!')
        return self.open_main_widget()

    def open_main_widget(self):
        """Открываем новый виджет"""
        self.main_screen = main_screen.MainScreen(self.id_)
        self.main_screen.show()
        self.close()

    def back(self):
        self.main_screen = main_screen.MainScreen(self.id_)
        self.main_screen.show()
        self.close()
