# -*- coding: utf-8 -*-
"""
    Main
    author: modorigoon
    since: 0.1.0
"""
import sys
import atexit
from common.logger import log
from common.config import get_config, get_opts
from PyQt5.QtWidgets import *
from lib.window import Window
from application import Application


class MainGui:

    def __init__(self):
        self._API_CONFIG = get_config('1q_api')
        self._window = Window(get_config('node_name'))
        self._app = Application(self._window)

    def exec(self, start=False):
        """ execution
        :return: void
        """
        try:
            self._window.set_real_name(self._API_CONFIG['target']['real_name'])
            self._window.set_symbol_name(self._API_CONFIG['target']['symbol'])
            self._window.append_log('[run] Initialize main application.')
            self._window.set_quit_button_listener(self.quit)
            self._window.set_run_button_listener(self.run)
            self._window.open_window()
            if start is True:
                self.run()
        except Exception as _e:
            self._window.append_log('[exec] ERROR: {}'.format(str(_e)))

    def stop(self):
        """ stop
        :return: void
        """
        try:
            self._window.append_log('[stop] service stopping..')
            self._window.set_run_button_text('STOPPING..')
            self._window.delete_run_button_listener()
            self._app.disconnect()
            self._window.append_log('[stop] service stop complete.')
        except Exception as _e:
            self._window.append_log('[stop] ERROR: {}'.format(str(_e)))
        finally:
            self._window.set_run_button_text('START')
            self._window.set_run_button_listener(self.run)

    def quit(self):
        """ quit application
        :return: void
        """
        self.stop()
        self._window.close_window()
        sys.exit()

    def run(self):
        """ start
        :return: void
        """
        try:
            self._window.set_run_button_text('STARTING..')
            self._window.delete_run_button_listener()
            self._app.connect()
            self._window.set_run_button_text('STOP')
            self._window.set_run_button_listener(self.stop)
            self._app.listen_real()
        except Exception as _e:
            self._window.append_log('[run] ERROR: {}'.format(str(_e)))
            self.stop()


app = QApplication(sys.argv)
opts = get_opts()
auto_start = False
if 's' in opts:
    auto_start = True
main_gui = MainGui()


def main():
    try:
        main_gui.exec(auto_start)
        sys.exit(app.exec_())
    except Exception as _e:
        log.error(str(_e))


def at_exit():
    if main_gui is not None:
        log.info('[exit] quit application.')
        main_gui.quit()


atexit.register(at_exit)


if __name__ == "__main__":
    main()
