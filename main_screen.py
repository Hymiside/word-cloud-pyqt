from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QComboBox

import service
import authentication
import tutorial
import update_profile


class MainScreen(QWidget):

    def __init__(self, id_):
        super().__init__()

        self.id_ = id_
        self.items = self.show_saved_pattern()

        self.initUI(self.items)
        self.setFixedSize(500, 590)

    def initUI(self, items):
        self.ex_ = QPushButton('Редактировать профиль', self)
        self.ex_.resize(400, 30)
        self.ex_.move(50, 520)
        self.ex_.setStyleSheet('.QPushButton { font-size: 11pt; }')
        self.ex_.clicked.connect(self.update_profile)

        self.ex_ = QPushButton('Выйти', self)
        self.ex_.resize(85, 30)
        self.ex_.move(364, 485)
        self.ex_.setStyleSheet('.QPushButton { font-size: 11pt; }')
        self.ex_.clicked.connect(self.exit)

        self.gnrt = QPushButton('Сгенерировать новый паттерн', self)
        self.gnrt.resize(280, 30)
        self.gnrt.move(50, 485)
        self.gnrt.setStyleSheet('.QPushButton { font-size: 11pt; }')
        self.gnrt.clicked.connect(self.generate_new_pattern)

        self.name_pattern = QLineEdit(self)
        self.name_pattern.resize(400, 40)
        self.name_pattern.move(50, 385)
        self.name_pattern.setPlaceholderText('Новый паттерн')

        self.combo = QComboBox(self)
        self.combo.addItems(items)
        self.combo.move(50, 320)
        self.combo.resize(400, 40)
        self.combo.activated[str].connect(self.generate_saved_pattern)

        self.text = QLabel(self)
        self.text.setText("Ваши паттерны")
        self.text.move(50, 290)
        self.text.setStyleSheet('.QLabel { font-size: 12pt; font-weight: '
                                'Bold }')

        self.text = QLabel(self)
        self.text.setText("Введите название нового паттерна\nили выберите "
                          "готовый из списка")
        self.text.move(50, 210)
        self.text.setStyleSheet('.QLabel { font-size: 13pt; font-weight: '
                                'Bold }')

        self.btn = QPushButton('Инструкция', self)
        self.btn.resize(400, 34)
        self.btn.move(50, 110)
        self.btn.setStyleSheet('.QPushButton { font-size: 11pt; }')
        self.btn.clicked.connect(self.open_tutorial)

        self.text = QLabel(self)
        self.text.setText("Перед использованием,\nознакомьтесь с инструкцией")
        self.text.move(50, 40)
        self.text.setStyleSheet('.QLabel { font-size: 15pt; font-weight: '
                                'Bold }')

        # Параметры окна
        self.setWindowTitle('WordPatterns')
        self.show()

    def generate_new_pattern(self):
        pattern = self.name_pattern.text()
        if pattern == "":
            return QtWidgets.QMessageBox.warning(self, 'Ошибка',
                                                 'Введите название паттерна!')
        QtWidgets.QMessageBox.warning(self, 'Уведомление',
                                      'Генерация началась! Ожидайте '
                                      'уведомления.')

        self.status = {'success': False}
        self.response = service.generate_new_pattern(pattern, self.id_,
                                                     self.status)

        if not self.response:
            return QtWidgets.QMessageBox.warning(self, 'Уведомление',
                                                 'Произошла ошибка попробуйте '
                                                 'еще раз!')
        self.combo.addItem(pattern)
        return QtWidgets.QMessageBox.warning(self, 'Уведомление',
                                             'Ваш паттерн готов!')

    def generate_saved_pattern(self):
        saved_pattern = self.combo.currentText()
        QtWidgets.QMessageBox.warning(self, 'Уведомление',
                                      'Генерация началась! Ожидайте '
                                      'уведомления.')
        self.status = {'success': False}
        service.generate_saved_pattern(saved_pattern,
                                       self.status)

        return QtWidgets.QMessageBox.warning(self, 'Уведомление',
                                             'Ваш паттерн готов!')

    def show_saved_pattern(self):
        response = service.show_saved_pattern(self.id_)
        return response

    def exit(self):
        self.auth_ = authentication.Authentication()
        self.auth_.show()
        self.close()

    def update_profile(self):
        self.auth_ = update_profile.UpdateProfile(self.id_)
        self.auth_.show()
        self.close()

    def open_tutorial(self):
        self.auth_ = tutorial.Tutorial(self.id_)
        self.auth_.show()
        self.close()
