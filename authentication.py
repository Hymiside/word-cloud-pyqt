from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QWidget

import database
import service
import authorization
import main_screen


class Authentication(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setFixedSize(500, 530)

    def initUI(self):
        # Кнопка для перехода на регистрацию
        self.text_reg = QPushButton("Нажмите, чтобы зарегистрироваться", self)
        self.text_reg.move(132, 409)
        self.text_reg.setStyleSheet('.QPushButton { font-size: 10pt; }')
        self.text_reg.clicked.connect(self.open_authorization)

        # Инфо текст
        self.text = QLabel(self)
        self.text.setText("Введите данные для входа")
        self.text.move(65, 75)
        self.text.setStyleSheet('.QLabel { font-size: 20pt; font-weight: '
                                'Bold }')

        # Кнопка войти
        self.btn = QPushButton('Войти', self)
        self.btn.resize(200, 55)
        self.btn.move(150, 339)
        self.btn.setStyleSheet('.QPushButton { font-size: 15pt; }')
        self.btn.clicked.connect(self.validation_data)

        # Форма для пароля
        self.password = QLineEdit(self)
        self.password.resize(400, 50)
        self.password.move(50, 239)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText('Пароль')

        # Форма для логина
        self.login = QLineEdit(self)
        self.login.resize(400, 50)
        self.login.move(50, 174)
        self.login.setPlaceholderText('Логин')

        # Параметры окна
        self.setWindowTitle('WordPatterns')
        self.show()

    def validation_data(self):
        """Валидации данных в формы"""
        login = self.login.text()
        password = self.password.text()

        response = service.validation_signin(login, password)
        if not response:
            return QtWidgets.QMessageBox.warning(self, 'Ошибка',
                                                 'Неверные данные!')

        id_ = database.get_user_id(login)
        return self.open_main_widget(id_)

    def open_authorization(self):
        """Открываем виджет регистрации"""
        self.auth = authorization.Authorization()
        self.auth.show()
        self.close()

    def open_main_widget(self, id_):
        """Открываем виджет главной страницы"""
        self.main_screen = main_screen.MainScreen(id_)
        self.main_screen.show()
        self.close()

