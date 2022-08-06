# -*- coding: utf-8 -*-
"""
    Window handler
    author: modorigoon
    since: 0.1.0
"""
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Window(QMainWindow):

    _WINDOW_TITLE_TEXT = 'TRADE TRANSACTION COLLECTOR'

    _WINDOW_TOP_POSITION = 300
    _WINDOW_LEFT_POSITION = 300

    _WINDOW_WIDTH_SIZE = 500
    _WINDOW_HEIGHT_SIZE = 500

    _LOGO_PATH = 'resource/logo.png'
    _LOGO_WIDTH_SIZE = 185
    _LOGO_HEIGHT_SIZE = 45

    def __init__(self, name=''):
        super().__init__()

        self._name = name
        self._real_text = None
        self._symbol_text = None
        self._log_text = None
        self._run_button = None
        self._quit_button = None
        self._last_transaction_text = None
        self._received_at_text = None

        self.init_base_ui()

    def init_base_ui(self):
        """ initialize base UI
        :return: void
        """
        self.setWindowTitle('{} ({})'.format(self._WINDOW_TITLE_TEXT, self._name))
        self.setStyleSheet("QMainWindow {background: 'black';}")
        self.setFixedSize(self._WINDOW_WIDTH_SIZE, self._WINDOW_HEIGHT_SIZE)
        self.move(self._WINDOW_TOP_POSITION, self._WINDOW_LEFT_POSITION)

        # LOGO
        logo = QPixmap(self._LOGO_PATH).scaledToWidth(self._LOGO_WIDTH_SIZE).scaledToHeight(self._LOGO_HEIGHT_SIZE)
        logo_label = QLabel(self)
        logo_label.setFixedWidth(self._LOGO_WIDTH_SIZE)
        logo_label.setFixedHeight(self._LOGO_HEIGHT_SIZE)
        logo_label.setPixmap(logo)
        logo_label.move(20, 20)

        bold_font = QFont('Verdana', 9)
        bold_font.setBold(True)

        bold_font_palette = QPalette()
        bold_font_palette.setColor(QPalette.WindowText, Qt.green)

        # REAL
        real_label = QLabel(self)
        real_label.setFont(bold_font)
        real_label.setPalette(bold_font_palette)
        real_label.setText("REAL NAME")
        real_label.move(20, 90)

        self._real_text = QLineEdit(self)
        self._real_text.setFixedWidth(80)
        self._real_text.setFont(QFont('Verdana', 9))
        self._real_text.move(110, 90)

        # SYMBOL
        symbol_label = QLabel(self)
        symbol_label.setFont(bold_font)
        symbol_label.setPalette(bold_font_palette)
        symbol_label.setText("SYMBOL")
        symbol_label.move(250, 90)

        self._symbol_text = QLineEdit(self)
        self._symbol_text.setFixedWidth(150)
        self._symbol_text.setFont(QFont('Verdana', 9))
        self._symbol_text.move(320, 90)

        # RECEIVE EVENT
        last_transaction_label = QLabel(self)
        last_transaction_label.setFont(bold_font)
        last_transaction_label.setFixedWidth(150)
        last_transaction_label.setPalette(bold_font_palette)
        last_transaction_label.setText("TRANSACTION")
        last_transaction_label.move(20, 130)

        self._last_transaction_text = QLineEdit(self)
        self._last_transaction_text.setFixedWidth(340)
        self._last_transaction_text.setFont(QFont('Verdana', 9))
        self._last_transaction_text.move(130, 130)

        # EVENT DATE TIME
        last_received_at_label = QLabel(self)
        last_received_at_label.setFont(bold_font)
        last_received_at_label.setFixedWidth(180)
        last_received_at_label.setPalette(bold_font_palette)
        last_received_at_label.setText("RECEIVED AT")
        last_received_at_label.move(20, 170)

        self._received_at_text = QLineEdit(self)
        self._received_at_text.setFixedWidth(300)
        self._received_at_text.setFont(QFont('Verdana', 9))
        self._received_at_text.move(130, 170)

        # LOG
        self._log_text = QTextEdit(self)
        self._log_text.setFixedSize(self._WINDOW_WIDTH_SIZE - 50, (self._WINDOW_HEIGHT_SIZE / 2) - 30)
        self._log_text.setFont(QFont('Verdana', 9))
        self._log_text.move(20, 210)

        # START
        self._run_button = QPushButton('START', self)
        self._run_button.setFont(bold_font)
        self._run_button.move(240, 450)

        # QUIT
        self._quit_button = QPushButton('QUIT', self)
        self._quit_button.setFont(bold_font)
        self._quit_button.move(370, 450)

    def open_window(self):
        """ open main window
        :return: void
        """
        self.show()

    def close_window(self):
        """ close main window
        :return: void
        """
        self.hide()

    def set_run_button_listener(self, sl):
        """ register run button listener
        :param sl: run button listener
        :return: void
        """
        self._run_button.clicked.connect(sl)

    def delete_run_button_listener(self):
        """ unregister run button listener
        :return: void
        """
        if self._run_button is not None:
            self._run_button.clicked.disconnect()

    def set_run_button_text(self, text: str):
        """ change text in run button
        :param text: run button text
        :return: void
        """
        self._run_button.setText(text)

    def set_quit_button_listener(self, ql):
        """ register quit button listener
        :param ql: quit button listener
        :return: void
        """
        self._quit_button.clicked.connect(ql)

    def set_quit_button_text(self, text: str):
        """ change text in quit button
        :param text: quit button text
        :return: void
        """
        self._quit_button.setText(text)

    def set_real_name(self, name: str):
        """ set REAL name
        :param name: REAL NAME
        :return: void
        """
        self._real_text.setText(name)

    def set_symbol_name(self, name: str):
        """ set SYMBOL
        :param name: SYMBOL
        :return: void
        """
        self._symbol_text.setText(name)

    def set_last_transaction(self, transaction: str):
        """set last event (transaction)
        :param transaction: transaction event
        :return: void
        """
        self._last_transaction_text.setText(transaction)

    def set_received_at(self, received_at: datetime):
        """ set last received date time
        :param received_at: received date time
        :return: void
        """
        self._received_at_text.setText(received_at.strftime('%Y-%m-%d %H:%M:%S'))

    def append_log(self, message: str):
        """ add log message
        :param message: log message
        :return: void
        """
        self._log_text.append(message)
