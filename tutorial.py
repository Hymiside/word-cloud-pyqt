from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel

import main_screen


class Tutorial(QWidget):

    def __init__(self, id_):
        super().__init__()

        self.id_ = id_

        self.initUI()
        self.setFixedSize(500, 530)

    def initUI(self):
        # Инфо текст
        self.btn = QPushButton('Назад', self)
        self.btn.resize(85, 30)
        self.btn.move(50, 430)
        self.btn.setStyleSheet('.QPushButton { font-size: 13pt; }')
        self.btn.clicked.connect(self.back)

        self.text = QLabel(self)
        self.text.setText("Инструкция")
        self.text.move(50, 45)
        self.text.setStyleSheet('.QLabel { font-size: 17pt; font-weight: '
                                'Bold }')

        self.text = QLabel(self)
        self.text.setText("1. Откройте приложение Telegram Desktop\nи "
                          "переписку для которой хотите сгенерировать\n"
                          "паттерн.\n\n2. В "
                          "правом верхнем углу найдите три точки\nи нажмите на "
                          "них.\n\n3. Выберите пункт Export chat history.\n\n"
                          "4. Уберите галочки со всех пунктов, в формате\n"
                          "экспорта выберите JSON и нажмите Export.\n\n"
                          "5. После экспорта скопируйте файл переписки\n"
                          "result.json в корень папки проекта\nи запустите "
                          "генерацию.")
        self.text.move(50, 110)
        self.text.setStyleSheet('.QLabel { font-size: 12pt;}')


        # Параметры окна
        self.setWindowTitle('WordPatterns')
        self.show()

    def back(self):
        self.main_screen = main_screen.MainScreen(self.id_)
        self.main_screen.show()
        self.close()
