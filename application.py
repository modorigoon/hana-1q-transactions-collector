# -*- coding: utf-8 -*-
"""
    Application
    author: modorigoon
    since: 0.1.0
"""
import os
from common.config import get_config
from common.logger import log, logging
from lib.hana_api import HanaAPI
from lib.transaction_processor import TransactionProcessor
import util.datetime_util as datetime_util


class Application:

    def __init__(self, window=None):
        """ constructor
        :param window: window handler
        """
        self._API_CONFIG = get_config('1q_api')
        self._api = HanaAPI(self._API_CONFIG)
        self._transaction_processor = TransactionProcessor()
        self._window = window

    def _log(self, level, message):
        """ logger
        :param level: log level
        :param message: log message
        :return: void
        """
        log.log(level, str(message))
        if self._window is not None:
            if logging.getLevelName(level) == 'ERROR':
                message = 'ERROR: ' + str(message)
            self._window.append_log(message)

    def get_connection_state(self) -> bool:
        """ check API connection status
        :return: connection status
        """
        comm_state = self._api.get_comm_state()
        if comm_state is False:
            self._log(logging.ERROR, '[get_connection_state] Communication module is not connected. ({})'
                      .format(str(comm_state)))
            return False
        has_session = self._api.get_login_state()
        if has_session is False:
            self._log(logging.ERROR, '[get_connection_state] Login session has ended.')
            return False
        return True

    def disconnect(self):
        """ disconnect
        :return: void
        """
        is_connected = self.get_connection_state()
        logout_successful = False
        if is_connected is True:
            logout_successful = self._api.logout()
        self._log(logging.INFO, '[disconnect] Logout successful: {}'.format(str(logout_successful)))
        unregister_successful = self._api.unregister_real_all()
        self._log(logging.INFO, '[disconnect] Unregister successful: {}'.format(str(unregister_successful)))
        self._api.terminate()

    def connect(self):
        """ connect
        :return: void
        """
        init_comm_result = self._api.comm_init()
        self._log(logging.INFO, '[connect] Initialize communication module result: {}'.format(str(init_comm_result)))
        if init_comm_result is False:
            raise Exception('[connect] Initialize communication module failed.')

        # 1st login attempt (expect failure)
        set_login_mode_result = self._api.set_login_mode(0, 1)
        login_successful = self._api.login()
        self._log(logging.INFO, '[connect] 1st try login process. [set mode: {}, login: {}]'
                  .format(str(set_login_mode_result), str(login_successful)))

        # 2nd login attempt (expect success)
        self._api.set_login_mode(0, 0)
        login_successful = self._api.login()
        if login_successful is False:
            raise Exception('[connect] Login process failed.')

        login_state = self._api.get_login_state()
        self._log(logging.INFO, '[connect] Login process successful. [login: {}, state: {}]'
                  .format(str(login_successful), str(login_state)))

    # -------------------------------------------------------------------------------------------------
    # REAL PART
    # -------------------------------------------------------------------------------------------------

    def on_receive_real_event(self, message):
        """ receive REAL EVENT
        :param message: EVENT message
        :return: void
        """
        transaction = self._transaction_processor.process(message)
        self._meta.set_meta('EVENT_AT', transaction['date_time_seq'])
        self._window.set_received_at(datetime_util.datetime_sequence_to_datetime(transaction['date_time_seq']))
        if self._window is not None:
            if transaction['id'] is not None:
                self._window.set_last_transaction('ID: {}, VALUE: {}'.format(str(transaction['id']),
                                                                             str(transaction['price'])))
            else:
                self._window.set_last_transaction('GENERATED TRANSACTION ID DUPLICATED.')

    def listen_real(self):
        """ listen REAL
        :return: void
        """
        self._api.set_real_event_handler(self.on_receive_real_event)
        register_real = self._api.register_real()
        self._log(logging.INFO, '[listen_real] Register real: {}'.format(str(register_real)))
        self._api.get_real_output_data()

    # -------------------------------------------------------------------------------------------------
    # FID PART
    # -------------------------------------------------------------------------------------------------

    def create_request_id(self):
        """ create request id
        :return: request id
        """
        request_id = self._api.create_request_id()
        log.info('[create_request_id] Request id created: {}'.format(str(request_id)))
        return request_id

    def release_request_id(self, rid):
        """ release request ID
        :param rid: request id
        :return: void
        """
        self._api.release_request_id(rid)

    def init_fid(self, rid):
        """ initialize FID
        :param rid: request id
        :return: initialize successful
        """
        f = self._api.set_fid_input(rid, '9001', 'FX')
        s = self._api.set_fid_input(rid, '9002', 'D05GBP/AUD')
        g = self._api.set_fid_input(rid, 'GID', '1003')
        t = self._api.set_fid_input(rid, '9119', '1')
        return f and s and g and t

    def set_fid_date_range(self, rid, start_date_seq: str, end_date_seq: str):
        """ set search period
        :param rid: request id
        :param start_date_seq: start date (ex: 20200302)
        :param end_date_seq: end date (ex: 20200302)
        :return:  set period successful
        """
        s = self._api.set_fid_input(rid, '9034', start_date_seq)
        e = self._api.set_fid_input(rid, '9035', end_date_seq)
        return s and e

    def request_fid(self, rid):
        """ request FID
        :param rid: request id
        :return: fid number
        """
        # FIELD
        # 8: TIME
        # 9: DATE
        # 1098: SELL SIGN
        # 30: SELL START PRICE
        # 31: SELL HIGH PRICE
        # 32: SELL LOW PRICE
        # 33: SELL CLOSE PRICE
        # 6: BUY SIGN
        # 40: BUY START PRICE
        # 41: BUY HIGH PRICE
        # 42: BUY LOW PRICE
        # 43: BUY CLOSE PRICE
        # 666: SPREAD
        fields = '8,9,30,31,32,33,6,40,41,42,43,1098,666'
        return self._api.request_fid_data_list(rid, fields, '1', '', 9999, 9999)

    def get_fid_output_data(self, rid, fid_code, row):
        """ return FID request output
        :param rid: request id
        :param fid_code: FID CODE (ref. request_fid method comment)
        :param row: row index
        :return: response output
        """
        return self._api.get_fid_output_data(rid, fid_code, row)

    def get_fid_response_count(self, rid):
        """ get count of FID response data
        :param rid: request id
        :return: count of FID response
        """
        return self._api.get_fid_output_count(rid)
